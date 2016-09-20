from rest_framework import serializers

from models import Portfolio, Transaction, Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('ticker', 'quantity')


class PortfolioSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    stocks = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'cash', 'owner', 'stocks', 'created')
        read_only_fields = ('cash', 'created')


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')])

    class Meta:
        model = Transaction
        fields = ('ticker', 'transaction_type', 'price', 'time', 'quantity', 'portfolio')
        read_only_fields = ('portfolio', 'time', 'price')
