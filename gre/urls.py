from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.GreIndex.as_view(), name='index'),
    url(r'^meaning/(?P<pword>[a-z]+)$', views.GreMeaning.as_view(), name='meaning'),
    url(r'^tag/$',views.GreAllTag.as_view(), name='alltag'),
    url(r'^tag/(?P<ptag>[\w]+)$',views.GreTag.as_view(),name='tag'),
    url(r'^words/$',views.TestScrap.as_view(),name='test'),
]
