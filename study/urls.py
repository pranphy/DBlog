from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.StudyIndex.as_view(), name='index'),
    #url(r'^detail/(?P<pslug>[\w-]+)$', views.BlogDetail.as_view(), name='detail'),
    #url(r'^download$',views.BlogDownload.as_view(), name="download"),
]
