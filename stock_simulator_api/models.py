import re
import datetime as dt

from django.db import models
from yahoo_finance.yql import YQLQuery


attributes = {
    'numeric': [
        'Ask', 'AverageDailyVolume', 'Bid', 'BookValue', 'Change',
        'ChangeFromFiftydayMovingAverage', 'ChangeFromTwoHundreddayMovingAverage',
        'ChangeFromYearHigh', 'ChangeFromYearLow', 'ChangeinPercent', 'DaysHigh',
        'DaysLow', 'DividendPayDate', 'DividendShare', 'DividendYield', 'EBITDA',
        'EPSEstimateCurrentYear', 'EPSEstimateNextQuarter', 'EPSEstimateNextYear',
        'EarningsShare', 'ExDividendDate', 'FiftydayMovingAverage', 'LastTradeDate',
        'LastTradePriceOnly', 'LastTradeTime', 'MarketCapitalization', 'OneyrTargetPrice',
        'PEGRatio', 'PERatio', 'PercebtChangeFromYearHigh', 'PercentChange',
        'PercentChangeFromFiftydayMovingAverage', 'PercentChangeFromTwoHundreddayMovingAverage',
        'PercentChangeFromYearLow', 'PreviousClose', 'PriceBook',
        'PriceEPSEstimateCurrentYear', 'PriceEPSEstimateNextYear',
        'PriceSales', 'ShortRatio', 'TwoHundreddayMovingAverage', 'Volume',
        'YearHigh', 'YearLow'
    ],
    'string': [
        'Currency', 'Name', 'StockExchange', 'Symbol'
    ]
}


def clean(key, value):
    """
    Cleans up a data point provided from yahoo_finance API.
    :param key: the name of the data point
    :param value: a value provided from yahoo_finance API
    :return: the cleaned version of value
    """
    if key in attributes['numeric']:
        if value is None:
            return value
        if 'B' in value:
            return float(value[:-1])*1000000000
        elif 'M' in value:
            return float(value[:-1])*1000000
        elif '%' in value:
            return float(value.strip('%'))
        elif '/' in value:
            return dt.datetime.strptime(value, '%m/%d/%Y').date()
        elif ':' in value:
            return dt.datetime.strptime(value, '%I:%M%p').time()
        elif '.' not in value:
            return int(value)
        else:  # value is string version of a float
            return float(value)
    elif key in attributes['string']:
        return value


class Portfolio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    cash = models.FloatField(default=100000)
    owner = models.ForeignKey('auth.User', related_name='portfolios')


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')


class Transaction(models.Model):
    ticker = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    price = models.FloatField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Quote(object):
    def __init__(self, ticker):
        results_dict = YQLQuery().execute(
            'SELECT * FROM yahoo.finance.quotes WHERE symbol="{}"'.format(ticker)
        )['query']['results']['quote']
        for key, value in results_dict.iteritems():
            if key in attributes['numeric'] or key in attributes['string']:
                # Yahoo Finance python API has typo for this attribute
                if key == 'PercebtChangeFromYearHigh':
                    attribute_name = 'percent_change_from_year_high'
                else:
                    attribute_name = '_'.join(re.findall('[A-Z][^A-Z]*', key)).lower()
                setattr(self, attribute_name, clean(key, value))
            else:
                continue
        if self.last_trade_date is None:
            raise Quote.InvalidTickerException

    class InvalidTickerException(Exception):
        pass
