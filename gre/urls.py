from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='gre'),
    url(r'^meaning/(?P<pword>[a-z]+)$', views.detail, name='meaning'),
    url(r'^tag/(?P<ptag>[\w]+)$',views.tag,name='tag')
    #url(r'^.+$',views.handler404, name="404"),
]
