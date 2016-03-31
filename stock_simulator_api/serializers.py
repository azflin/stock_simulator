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
        fields = ('id', 'name', 'cash', 'owner', 'stocks')
        read_only_fields = ('cash', )


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')])

    class Meta:
        model = Transaction
        fields = ('ticker', 'transaction_type', 'price', 'time', 'quantity', 'portfolio')
        read_only_fields = ('portfolio', 'time', 'price')


class QuoteSerializer(serializers.Serializer):
    ask = serializers.FloatField()
    average_daily_volume = serializers.IntegerField()
    bid = serializers.FloatField()
    book_value = serializers.FloatField()
    change = serializers.FloatField()
    change_from_fiftyday_moving_average = serializers.FloatField()
    change_from_two_hundredday_moving_average = serializers.FloatField()
    change_from_year_high = serializers.FloatField()
    change_from_year_low = serializers.FloatField()
    changein_percent = serializers.FloatField()
    currency = serializers.CharField()
    days_high = serializers.FloatField()
    days_low = serializers.FloatField()
    dividend_pay_date = serializers.DateField()
    dividend_share = serializers.FloatField()
    dividend_yield = serializers.FloatField()
    e_b_i_t_d_a = serializers.IntegerField()
    e_p_s_estimate_current_year = serializers.FloatField()
    e_p_s_estimate_next_quarter = serializers.FloatField()
    e_p_s_estimate_next_year = serializers.FloatField()
    earnings_share = serializers.FloatField()
    ex_dividend_date = serializers.DateField()
    fiftyday_moving_average = serializers.FloatField()
    last_trade_date = serializers.DateField()
    last_trade_price_only = serializers.FloatField()
    last_trade_time = serializers.TimeField()
    market_capitalization = serializers.IntegerField()
    name = serializers.CharField()
    oneyr_target_price = serializers.FloatField()
    p_e_g_ratio = serializers.FloatField()
    p_e_ratio = serializers.FloatField()
    percent_change_from_year_high = serializers.FloatField()
    percent_change = serializers.FloatField()
    percent_change_from_fiftyday_moving_average = serializers.FloatField()
    percent_change_from_two_hundredday_moving_average = serializers.FloatField()
    percent_change_from_year_low = serializers.FloatField()
    previous_close = serializers.FloatField()
    price_book = serializers.FloatField()
    price_e_p_s_estimate_current_year = serializers.FloatField()
    price_e_p_s_estimate_next_year = serializers.FloatField()
    price_sales = serializers.FloatField()
    short_ratio = serializers.FloatField()
    stock_exchange = serializers.CharField()
    symbol = serializers.CharField()
    two_hundredday_moving_average = serializers.FloatField()
    volume = serializers.IntegerField()
    year_high = serializers.FloatField()
    year_low = serializers.FloatField()