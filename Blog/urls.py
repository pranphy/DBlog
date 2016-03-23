from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog/download$',views.download, name="download"),
    url(r'^(?P<pslug>[\w-]+)$', views.detail, name='detail'),
]
