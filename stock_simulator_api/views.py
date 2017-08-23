import requests
import urllib

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
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
    encoded_tickers = urllib.quote("'" + tickers + "'")
    url_query = (
        "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20"
        "where%20symbol%20in%20({})&format=json&diagnostics=true&"
        "env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    )
    content = requests.get(url_query.format(encoded_tickers)).json()
    content = content['query']['results']['quote']
    # If single quote requested, the returned json will be a dict. If multiple quotes requested,
    # returned json will be a list. So convert the dict to a list in the single quote case.
    if type(content) == dict:
        content = [content]
    quotes_to_return = {}
    for quote in content:
        # Invalid tickers will have a None LastTradePriceOnly
        if not quote['LastTradePriceOnly']:
            continue
        change = round(float(quote['Change']), 2)
        price = round(float(quote['LastTradePriceOnly']), 2)
        quotes_to_return[quote['Symbol']] = {
            'change': change,
            'change_percent': round((price / (price - change) - 1) * 100, 2),
            'day_high': round(float(quote['DaysHigh']), 2),
            'day_low': round(float(quote['DaysLow']), 2),
            'name': quote['Name'],
            'price': price,
            'volume': int(quote['Volume']),
            'year_high': round(float(quote['YearHigh']), 2),
            'year_low': round(float(quote['YearLow']), 2)
        }
    return quotes_to_return


class GetQuotes(APIView):
    """
    /api/quote/<tickers>/
        GET: Get quote information on a list of tickers. Returns JSON response of a dict with keys
        being tickers and values being a dict of quote information.
    """
    def get(self, request, tickers):
        quotes = get_yahoo_quote(tickers)
        return JsonResponse(quotes)


class PortfolioViewSet(viewsets.ModelViewSet):
    """
    /api/portfolios/
        GET: Get all portfolios. If a username query parameter is passed, then get that user's
        portfolios.
        POST: Create a portfolio. Must be authenticated. JSON payload must contain "name".

    /api/portfolios/<portfolio_id>/
        GET: Get one portfolio.
        PUT: Edit a portfolio (can only edit name). Must be authenticated as owner of portfolio.
        DELETE: Delete a portfolio. Must be authenticated as owner of portfolio.
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

    # list can be filtered by username, otherwise return all portfolios
    def list(self, request):
        username = request.query_params.get('username', None)
        if username:
            user = User.objects.filter(username=username)
            queryset = Portfolio.objects.filter(owner=user)
        else:
            queryset = Portfolio.objects.all()
        serializer = PortfolioSerializer(queryset, many=True)
        return Response(serializer.data)


class TransactionsList(generics.ListCreateAPIView):
    """
    /api/portfolios/<portfolio_id>/transactions/
        GET: Get list of portfolio's transactions.
        POST: Create a transaction. Must be authenticated. JSON payload must contain:
            "ticker": Ticker of security you want to transact.
            "quantity": Number of units you want to transact.
            "transaction_type": Either "Buy" or "Sell"
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
    /api/portfolios/<portfolio_id>/stocks/
        GET: Get portfolio's stock holdings.
    """
    serializer_class = StockSerializer

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        return Stock.objects.filter(portfolio=p)


class UsersList(generics.ListAPIView):
    """
    /api/users/
        GET: Get all users.
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users
