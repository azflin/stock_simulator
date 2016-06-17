from django.db import models


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

