from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gre$',views.index, name='index'),
    url(r'^detail/(?P<pword>[a-z]+)$', views.detail, name='detail'),
    #url(r'^.+$',views.handler404, name="404"),
]
