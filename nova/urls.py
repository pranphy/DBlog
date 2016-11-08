from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NovaIndex.as_view(), name='index'),
]
