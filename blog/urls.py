from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BlogIndex.as_view(), name='index'),
    url(r'^detail/(?P<pslug>[\w-]+)$', views.BlogDetail.as_view(), name='detail'),
    url(r'^download$',views.BlogDownload.as_view(), name="download"),
]

handler404 = 'RBlog.views.handler404'
