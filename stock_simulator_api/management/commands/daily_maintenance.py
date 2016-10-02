"""
daily_maintenance.py contains functions required for the daily maintenance of the stock
simulator app, including saving end of day positions and checking for margin calls. These functions
are intended to be run as django management commands through the chron scheduler.
"""
from django.core.management.base import BaseCommand

from stock_simulator_api.models import Position, Portfolio
from stock_simulator_api.views import get_yahoo_quote


def force_margin_call(portfolio):
    """
    Determine if portfolio requires a margin call (short exposure > 150% of equity). If so,
    reduce short exposure by using cash to buy shorted stocks pro rata. If portfolio has
    insufficient cash, sell stocks pro rata to generate enough cash. If short exposure > equity ...
    disable account? IDK.
    """
    raise NotImplementedError


def save_positions(portfolio):
    """
    Create Positions for the portfolio. This function will be called at the end of each market
    day to capture that day's end of day prices.
    """
    # Save portfolio's stock positions
    for stock in portfolio.stocks.all():
        position = Position(
            ticker=stock.ticker,
            units=stock.quantity,
            price=get_yahoo_quote(stock.ticker)[stock.ticker]["price"],
            portfolio=stock.portfolio
        )
        position.save()
    # Save portfolio's cash position
    cash_position = Position(
        ticker='CASH',
        units=portfolio.cash,
        price=1,
        portfolio=portfolio
    )
    cash_position.save()


class Command(BaseCommand):
    help = 'Daily maintenance tasks for the stock simulator.'

    def add_arguments(self, parser):
        parser.add_argument('--save_positions', action='store_true')

    def handle(self, *args, **options):
        if options['save_positions']:
            for portfolio in Portfolio.objects.all():
                save_positions(portfolio)
                print "Saved positions for portfolio {}".format(portfolio.name)