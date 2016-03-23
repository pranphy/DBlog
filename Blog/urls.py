from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download$',views.download, name="download"),
    url(r'^detail/(?P<pslug>[\w-]+)$', views.detail, name='detail'),
    url(r'^.+$',views.handler404, name="404"),
]

handler404 = 'RBlog.views.handler404'
