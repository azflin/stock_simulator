from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from stock_simulator_api.models import Portfolio, Quote, Transaction, Stock
from stock_simulator_api.permissions import IsOwnerOrReadOnly
from serializers import QuoteSerializer, TransactionSerializer, StockSerializer
from serializers import PortfolioSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    """
    The portfolios attached to your account. Supports POST, GET list, GET individual.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # Request's user is saved as owner of portfolio
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Filtering against current user
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if not username:
            raise ValidationError("Must supply username.")
        user = User.objects.filter(username=username)
        if user:
            return Portfolio.objects.filter(owner=user)
        else:  # No such user exists
            raise ValidationError("No such user exists.")



class TransactionsList(generics.ListCreateAPIView):
    """
    The transactions attached to its portfolio. Supports POST, and GET list.
    """
    serializer_class = TransactionSerializer

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        return Transaction.objects.filter(portfolio=p)

    def perform_create(self, serializer):
        # Get URL parameter and query parameters
        portfolio = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        ticker = self.request.data['ticker'].upper()
        quantity = int(self.request.data['quantity'])
        transaction_type = self.request.data['transaction_type']

        quote = Quote(ticker)
        transaction_amount = quantity * quote.last_trade_price_only
        if transaction_type == 'Buy':
            # Check if portfolio has sufficient funds to execute transaction
            if transaction_amount > portfolio.cash:
                raise ValidationError(
                    'Insufficient cash to buy {} shares of {}'.format(
                        quantity,
                        ticker
                    )
                )
            portfolio.cash -= transaction_amount
            portfolio.save()
            # Check if ticker already exists in portfolio's stocks
            if ticker in [stock.ticker for stock in portfolio.stocks.all()]:
                stock_to_increase = portfolio.stocks.get(ticker=ticker)
                stock_to_increase.quantity += quantity
                stock_to_increase.save()
            else:  # ticker doesn't exist in portfolio, create new Stock
                new_stock = Stock(
                    ticker=ticker,
                    quantity=quantity,
                    portfolio=portfolio
                )
                new_stock.save()
        elif transaction_type == 'Sell':
            # Check if portfolio has sufficient units of stock to sell
            if ticker in [stock.ticker for stock in portfolio.stocks.all()]:
                stock_to_sell = portfolio.stocks.get(ticker=ticker)
                if stock_to_sell.quantity >= quantity:
                    stock_to_sell.quantity -= quantity
                    stock_to_sell.save()
                    if stock_to_sell.quantity == 0:
                        stock_to_sell.delete()
                    portfolio.cash += transaction_amount
                    portfolio.save()
                else:  # Portfolio doesn't have enough units of ticker to sell
                    raise ValidationError(
                        "You want to sell {} units of {} but only have {} units.".format(
                            quantity,
                            ticker,
                            stock_to_sell.quantity
                        )
                    )
            else:  # Ticker doesn't exist in portfolio's stocks
                raise ValidationError(
                    "{} doesn't exist in {}'s stocks.".format(
                        ticker,
                        portfolio.name
                    )
                )

        serializer.save(ticker=ticker, portfolio=portfolio, price=quote.last_trade_price_only)


class StocksList(generics.ListAPIView):
    """
    The stock holdings attached to a portfolio. Supports GET list.
    """
    serializer_class = StockSerializer

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        return Stock.objects.filter(portfolio=p)


@api_view(['GET'])
def quote_get(request, ticker):
    """
    Get a quote from yahoo finance's API.
    """
    try:
        quote = Quote(ticker)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)
    except Quote.InvalidTickerException:
        return Response({"Error": "This ticker does not exist in Yahoo Finance."})
