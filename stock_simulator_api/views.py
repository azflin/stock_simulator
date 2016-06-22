import requests

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse

from stock_simulator_api.models import Portfolio, Transaction, Stock
from stock_simulator_api.permissions import IsOwnerOrReadOnly, IsPortfolioOwnerOrReadOnly
from serializers import TransactionSerializer, StockSerializer
from serializers import PortfolioSerializer


def get_yahoo_quote(tickers):
    """
    get_yahoo_quote returns stock quote information from yahoo finance's webservice on the
    supplied tickers.

    :param tickers: string of comma separated tickers
    :return dict where key is string ticker and value is dict of ticker's quote info
    """
    url_query = "https://finance.yahoo.com/webservice/v1/symbols/{}/quote?format=json&view=detail"
    yahoo_quotes_response = requests.get(url_query.format(tickers)).json()
    quotes_to_return = {}
    for quote in yahoo_quotes_response['list']['resources']:
        ticker_dict = quote['resource']['fields']
        quotes_to_return[ticker_dict['symbol']] = {
            'change': round(float(ticker_dict['change']), 2),
            'change_percent': round(float(ticker_dict['chg_percent']), 2),
            'day_high': round(float(ticker_dict['day_high']), 2),
            'day_low': round(float(ticker_dict['day_low']), 2),
            'name': ticker_dict['name'],
            'price': round(float(ticker_dict['price']), 2),
            'volume': int(ticker_dict['volume']),
            'year_high': round(float(ticker_dict['year_high']), 2),
            'year_low': round(float(ticker_dict['year_low']), 2)
        }
    return quotes_to_return


class PortfolioViewSet(viewsets.ModelViewSet):
    """
    The portfolios belonging to an account provided by username get parameter.
    Supports POST, GET list, GET individual.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,  # Unauthenticated users cannot POST
        IsOwnerOrReadOnly  # Authenticated users that don't own portfolio cannot edit it
    )

    # Request's user is saved as owner of portfolio
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Get portfolios belonging to the username given in username get parameter
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if not username:
            raise ValidationError({"detail": "No username get parameter provided."})
        user = User.objects.filter(username=username)
        if user:
            return Portfolio.objects.filter(owner=user)
        else:  # No such user exists
            raise ValidationError({"detail": "No such user exists."})


class TransactionsList(generics.ListCreateAPIView):
    """
    The transactions attached to its portfolio. Supports POST, and GET list.
    """
    serializer_class = TransactionSerializer
    permission_classes = (IsPortfolioOwnerOrReadOnly, )

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        # Return transactions in reverse order to get most recent
        # transactions first.
        return Transaction.objects.filter(portfolio=p)[::-1]

    def perform_create(self, serializer):

        # Assign request data to local variables
        portfolio = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        ticker = self.request.data['ticker'].upper()
        requested_quantity = int(self.request.data['quantity'])
        if requested_quantity <= 0:
            raise ValidationError("Cannot transact negative units.")
        transaction_type = self.request.data['transaction_type']

        # Get price of ticker and total transaction amount
        price = get_yahoo_quote(ticker)[ticker]['price']
        transaction_amount = requested_quantity * price
        # Get the held stock if it already exists in the portfolio. Otherwise held_stock is None
        held_stock = portfolio.stocks.filter(ticker=ticker).first()

        if transaction_type == 'Buy':
            # Check if portfolio has sufficient funds to execute transaction
            if transaction_amount > portfolio.cash:
                raise ValidationError(
                    'Insufficient cash to buy {} shares of {}'.format(
                        requested_quantity,
                        ticker
                    )
                )
            portfolio.cash -= transaction_amount
            portfolio.save()
            if held_stock:
                held_stock.quantity += requested_quantity
                held_stock.save()
            else:  # ticker doesn't exist in portfolio, create new Stock
                new_stock = Stock(
                    ticker=ticker,
                    quantity=requested_quantity,
                    portfolio=portfolio
                )
                new_stock.save()

        elif transaction_type == 'Sell':
            # If you hold more units than you want to sell, proceed.
            if held_stock and held_stock.quantity >= requested_quantity:
                portfolio.cash += transaction_amount
                held_stock.quantity -= requested_quantity
                portfolio.save()
                held_stock.save()
            # Else we attempt to short and must check if equity > 150% short exposure
            else:
                short_exposure = portfolio.get_short_exposure()
                # If we don't have stock or have a short position in it, increase our short exposure
                # by transaction amount.
                if not held_stock or held_stock.quantity < 0:
                    short_exposure += transaction_amount
                # If we have stock but the sell transaction will move us into a short position,
                # add the remaining units to short exposure
                elif held_stock.quantity < requested_quantity:
                    short_exposure += (requested_quantity - held_stock.quantity) * price

                # If our equity is > 150% of short exposure, proceed with transaction
                if short_exposure * 1.5 < portfolio.get_market_value():
                    portfolio.cash += transaction_amount
                    portfolio.save()
                    if held_stock:
                        held_stock.quantity -= requested_quantity
                        if held_stock.quantity == 0:
                            held_stock.delete()
                        else:
                            held_stock.save()
                    else:  # Create new short stock position if not held
                        new_stock = Stock(
                            ticker=ticker,
                            quantity=-requested_quantity,
                            portfolio=portfolio
                        )
                        new_stock.save()
                else:
                    raise ValidationError(
                        ("Insufficient equity to short. ",
                         "Your equity must be 150% of your short exposure.")
                    )

        serializer.save(ticker=ticker, portfolio=portfolio, price=price)


class StocksList(generics.ListAPIView):
    """
    The stock holdings attached to a portfolio. Supports GET list.
    """
    serializer_class = StockSerializer

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        return Stock.objects.filter(portfolio=p)


@api_view(['GET'])
def get_quotes(request, tickers):
    """
    get_quotes returns stock price data for a given list of tickers in JSON format.
    It makes a call to yahoo finance's quotes webservice and reformats the response into
    a more usable format.

    :param request: Django request
    :param tickers: string in URL of comma separated tickers
    :return: JSON representation of a dict with keys being tickers and values being a dict
    of pricing data
    """

    quotes = get_yahoo_quote(tickers)
    return JsonResponse(quotes)

