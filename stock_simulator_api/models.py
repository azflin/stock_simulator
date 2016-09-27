from django.db import models


class Portfolio(models.Model):
    """
    A portfolio belonging to a User. A portfolio has a cash balance (defaulting to $100,000),
    stocks and transactions.
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    cash = models.FloatField(default=100000)
    owner = models.ForeignKey('auth.User', related_name='portfolios')

    def get_market_value(self):
        """
        Return portfolio's market value. This is sum of cash and market value of long positions.

        Returns:
            float: portfolio's market value
        """
        market_value = self.cash
        long_stocks = [stock for stock in self.stocks.all() if stock.quantity > 0]
        if long_stocks:
            long_stocks_tickers = ",".join([stock.ticker for stock in long_stocks])
            long_stocks_quote = get_yahoo_quote(long_stocks_tickers)
            for stock in long_stocks:
                market_value += long_stocks_quote[stock.ticker]['price'] * stock.quantity
        return market_value

    def get_short_exposure(self):
        """
        Return the portfolio's short exposure.

        Returns:
            float: portfolio's short exposure. 0 if no shorts.
        """
        shorted_stocks = self.stocks.filter(quantity__lt=0)
        if len(shorted_stocks) == 0:
            return 0
        shorted_stocks_tickers = ",".join([stock.ticker for stock in shorted_stocks])
        shorted_stocks_quote = get_yahoo_quote(shorted_stocks_tickers)
        short_exposure = sum(
            [-stock.quantity * shorted_stocks_quote[stock.ticker]['price']
             for stock in shorted_stocks]
        )
        return short_exposure


class Stock(models.Model):
    """
    A stock belonging to a Portfolio.
    """
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')


class Transaction(models.Model):
    """
    A transaction belonging to a Portfolio.
    """
    ticker = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    price = models.FloatField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Position(models.Model):
    """
    A position is a record of a Portfolio's stock holding on a given date.
    """
    datetime = models.DateTimeField(auto_now_add=True)
    ticker = models.CharField(max_length=50)
    units = models.IntegerField()
    price = models.FloatField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='positions')


# Must import after model definitions because of circular import error
from views import get_yahoo_quote
