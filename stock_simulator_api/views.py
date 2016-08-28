import requests

from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse

from stock_simulator_api.models import Portfolio, Transaction, Stock
from stock_simulator_api.permissions import IsOwnerOrReadOnly, IsPortfolioOwnerOrReadOnly
from authentication.serializers import UserSerializer
from serializers import TransactionSerializer, StockSerializer
from serializers import PortfolioSerializer


def get_yahoo_quote(tickers):
    """
    get_yahoo_quote returns stock quote information from yahoo finance's webservice on the
    supplied tickers.

    Args:
        tickers (str): Tickers delimited by commas
    Returns:
        Dict(str: Dict): The key is the ticker and the value is dict of ticker's quote info
    """
    url_query = "https://finance.yahoo.com/webservice/v1/symbols/{}/quote?format=json&view=detail"
    # Yahoo Finance's webservice has been shutdown, EXCEPT for when you add this mobile header.
    # This is currently a workaround, and eventually I will need to replace this entire process.
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MotoG3 Build/MPI24.107-55)" +
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.81 Mobile Safari/537.36"}
    yahoo_quotes_response = requests.get(url_query.format(tickers), headers=headers).json()
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


class GetQuotes(APIView):
    """
    Get quote information on a list of tickers. Returns JSON response of a dict with keys being
    tickers and values being a dict of quote information.
    """
    def get(self, request, tickers):
        quotes = get_yahoo_quote(tickers)
        return JsonResponse(quotes)


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
        transaction_amount = round(requested_quantity * price, 2)
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
                if held_stock.quantity == 0:
                    held_stock.delete()
                else:
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
                portfolio.save()
                held_stock.quantity -= requested_quantity
                if held_stock.quantity == 0:
                    held_stock.delete()
                else:
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
                equity = portfolio.get_market_value() + transaction_amount
                if short_exposure * 1.5 < equity:
                    portfolio.cash += transaction_amount
                    portfolio.save()
                    if held_stock:
                        held_stock.quantity -= requested_quantity
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
                        (
                            "This transaction will bring your equity to {0}, but your total "
                            "short exposure will be {1}. Your equity must be greater than "
                            "150% of your total short exposure to proceed."
                        ).format(equity, short_exposure)
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


class TopPortfoliosList(generics.ListAPIView):
    """
    List of top performing portfolios. Supports GET list.
    """
    serializer_class = PortfolioSerializer

    # TODO: Currently its just a brute force method
    def get_queryset(self):
        portfolios = Portfolio.objects.all()
        portfolios_with_mkt_values = []
        for portfolio in portfolios:
            portfolios_with_mkt_values.append({
                "portfolio": portfolio,
                "market_value": portfolio.get_market_value()
            })
        sorted_portfolios = sorted(portfolios_with_mkt_values, key=lambda x: x['market_value'])


class UsersList(generics.ListAPIView):
    """
    All the users in stock_simulator's database. Supports GET list.
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users
