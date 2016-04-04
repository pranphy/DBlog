from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='gre'),
    url(r'^meaning/(?P<pword>[a-z]+)$', views.meaning, name='meaning'),
    url(r'^tag/$',views.alltag, name='alltag'),
    url(r'^tag/(?P<ptag>[\w]+)$',views.tag,name='tag')
]
