from mock import patch
from django.test import Client, TestCase
from django.contrib.auth.models import User

from stock_simulator_api.models import Portfolio, Stock


class BuyTransactionTestCase(TestCase):

    def setUp(self):
        test_user = User.objects.create_user('test_user', password='test_password')
        self.p = Portfolio(owner=test_user)
        self.p.save()
        self.c = Client()
        self.c.login(username='test_user', password='test_password')

    @patch('stock_simulator_api.views.get_yahoo_quote')
    def test_buy_stock_success(self, mock_get_yahoo_quote):
        mock_get_yahoo_quote.return_value = {"TEST": {"price": 1}}
        self.c.post(
            "/api/portfolios/1/transactions/",
            data={
                "ticker": "TEST",
                "transaction_type": "Buy",
                "quantity": 100000
            }
        )
        self.assertTrue(self.p.stocks.filter(ticker="TEST").exists())
        s = self.p.stocks.get(ticker="TEST")
        self.assertEqual(s.quantity, 100000)

    @patch('stock_simulator_api.views.get_yahoo_quote')
    def test_buy_stock_fail(self, mock_get_yahoo_quote):
        """Test insufficient cash for buy transaction."""
        mock_get_yahoo_quote.return_value = {"TEST": {"price": 1}}
        r = self.c.post(
            "/api/portfolios/1/transactions/",
            data={
                "ticker": "TEST",
                "transaction_type": "Buy",
                "quantity": 100001
            }
        )
        self.assertEqual(r.status_code, 400)


class SellTransactionTestCase(TestCase):

    def setUp(self):
        test_user = User.objects.create_user('test_user', password='test_password')
        self.p = Portfolio(owner=test_user)
        self.p.save()
        self.c = Client()
        self.c.login(username='test_user', password='test_password')

    @patch('stock_simulator_api.views.get_yahoo_quote')
    def test_sell_existing_stock(self, mock_get_yahoo_quote):
        """
        Test you can sell an existing stock. Ensure the stock disappears from portfolio's stock list
        and our portfolio's cash is increased correctly.
        """
        mock_get_yahoo_quote.return_value = {"FOO": {"price": 1}}
        self.s_foo = Stock(
            ticker="FOO",
            quantity=1,
            portfolio=self.p
        )
        self.s_foo.save()
        self.assertTrue(self.p.stocks.filter(ticker="FOO").exists())
        self.c.post(
            "/api/portfolios/1/transactions/",
            data={
                "ticker": "FOO",
                "transaction_type": "Sell",
                "quantity": 1
            }
        )
        p = Portfolio.objects.get(pk=1)
        self.assertFalse(p.stocks.filter(ticker="FOO").exists())
        self.assertEqual(p.cash, 100001)

    @patch('stock_simulator_api.views.get_yahoo_quote')
    def test_short_new_stock(self, mock_get_yahoo_quote_views):
        """
        Test that you can short a new stock (stock doesn't exist in Portfolio's stocks). First
        attempt to short $199,999 worth of stock and ensure this succeeds, then attempt to short
        $200,000 worth of stock and ensure this fails. This is because equity must > 1.5 *
        short exposure to proceed, and we start with $100,000 equity.
        """
        mock_get_yahoo_quote_views.side_effect = [{"FOO": {"price": 1}}, {"FOO": {"price": 1}}]
        self.assertFalse(self.p.stocks.filter(ticker="FOO").exists())
        self.c.post(
            "/api/portfolios/1/transactions/",
            data={
                "ticker": "FOO",
                "transaction_type": "Sell",
                "quantity": 199999
            }
        )
        p = Portfolio.objects.get(pk=1)
        self.assertTrue(p.stocks.filter(ticker="FOO").exists())
        s = p.stocks.get(ticker="FOO")
        self.assertEqual(s.quantity, -199999)

        # Reset p to test for failure.
        p.cash = 100000
        s.delete()
        p.save()

        # Attempt to short $200,000 worth of stock, which does not satisfy our equity requirement
        r = self.c.post(
            "/api/portfolios/1/transactions/",
            data={
                "ticker": "FOO",
                "transaction_type": "Sell",
                "quantity": 200000
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertFalse(p.stocks.filter(ticker="FOO").exists())
