from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('stock_simulator_api.urls'))
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
