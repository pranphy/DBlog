from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

import datetime

from .models import Tag 
from .models import BlogPost
from .models import Comment 


def index(request):
    allposts = BlogPost.objects.all()
    template = loader.get_template('Blog/index.html')
    Repeat = [1,2]

    context   = {
        'Repeat' : Repeat,
        'allposts' : allposts,
    }
    return HttpResponse(template.render(context,request))

def detail(request,slug):
    currentpost = BlogPost.objects.get(id=slug) 
    template = loader.get_template('Blog/details.html')

    context = {
        'post': currentpost
    }

    return HttpResponse(template.render(context,request))
