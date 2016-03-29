from django.conf.urls import url, include

from views import IndexView

urlpatterns = [
    url(r'^api/', include('stock_simulator_api.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url('^$', IndexView.as_view(), name='index')
]
