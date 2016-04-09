from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.StudyIndex.as_view(), name='index'),
    url(r'^test/', views.TestView.as_view(), name='test'),
    url(r'^markdown/', views.MarkdownTest.as_view(), name='markdown'),
    #url(r'^detail/(?P<pslug>[\w-]+)$', views.BlogDetail.as_view(), name='detail'),
    #url(r'^download$',views.BlogDownload.as_view(), name="download"),
]
