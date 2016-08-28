from django.conf.urls import url, include
from stock_simulator_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'portfolios', views.PortfolioViewSet)

urlpatterns = [
    # Portfolio's ModelViewSet
    url(r'^', include(router.urls)),
    # Comma separated alphabetic strings representing a list of tickers
    url(r'^quote/(?P<tickers>[a-zA-Z]+(,[a-zA-Z]+)*)/$', views.GetQuotes.as_view()),
    # A portfolio's Transactions
    url(r'^portfolios/(?P<portfolio_id>[0-9]+)/transactions/$',
        views.TransactionsList.as_view(),
        name='portfolio-transactions'),
    # A portfolio's Stocks
    url(r'^portfolios/(?P<portfolio_id>[0-9]+)/stocks/$',
        views.StocksList.as_view(),
        name='portfolio-stocks'),
    # List of all Users
    url(r'^users/$', views.UsersList.as_view())
]