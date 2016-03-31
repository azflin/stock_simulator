from django.conf.urls import url, include
from stock_simulator_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'portfolios', views.PortfolioViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^quote/(?P<ticker>.*)/$', views.quote_get),
    url(r'^portfolios/(?P<portfolio_id>[0-9]+)/transactions/$',
        views.TransactionsList.as_view(),
        name='portfolio-transactions'),
    url(r'^portfolios/(?P<portfolio_id>[0-9]+)/stocks/$',
        views.StocksList.as_view(),
        name='portfolio-stocks'),
]