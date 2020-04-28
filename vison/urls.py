from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.VisonIndex.as_view(), name='index'),
    url(r'^graph$', views.VisonGraph.as_view(), name='graph'),
    #url(r'^meaning/(?P<pword>[a-z]+)$', views.GreMeaning.as_view(), name='meaning'),
]

