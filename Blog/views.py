from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from .models import News
from .models import NavigationItems
from .models import BlogPost
import datetime


def index(request):
    NewsGroup = News.objects.order_by("-Date")
    NavItems = NavigationItems.objects.all();
    template = loader.get_template('Blog/index.html')
    AllBlogPosts = BlogPost.objects.all(); 

    context   = {
        'NewsGroup' : NewsGroup,
        'NavItems'  : NavItems,
        'AllBlogPosts': AllBlogPosts,
    }
    return HttpResponse(template.render(context,request))

def dataGrid(request):
    template = loader.get_template('Blog/DataGrid.html');
    context = {}
    return HttpResponse(template.render(context,request))
