from django.conf.urls import url, include

from views import IndexView
from authentication.views import CreateUserView, LoginView, LogoutView

urlpatterns = [
    url(r'^api/register/$', CreateUserView.as_view()),
    url(r'^api/login/$', LoginView.as_view()),
    url(r'^api/logout/$', LogoutView.as_view()),
    url(r'^api/', include('stock_simulator_api.urls')),
    url('^$', IndexView.as_view(), name='index')
]
