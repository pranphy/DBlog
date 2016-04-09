"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin

#Adding the following two lines
from django.conf import settings
from django.conf.urls.static import static

import django.views.defaults

urlpatterns = [
    url(r'^blog/',include('Blog.urls', namespace='blog')),
    url(r'^gre/',include('gre.urls', namespace='gre')),
    url(r'^study/',include('study.urls', namespace='study')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('Blog.urls', namespace='blog')),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

#Adding +static.... resolved the issue
