from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.BlogIndex.as_view(), name='index'),
    url(r'^detail/(?P<pslug>[\w-]+)$', views.BlogDetail.as_view(), name='detail'),
    url(r'^download$',views.BlogDownload.as_view(), name="download"),
]

handler404 = 'blog.views.handler404'
