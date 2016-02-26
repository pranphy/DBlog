from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from .models import News
import datetime


def index(request):
    NewsGroup = News.objects.order_by("-Date")
    template = loader.get_template('Blog/index.html')

    context   = {
        'NewsGroup' : NewsGroup,
    }
    return HttpResponse(template.render(context,request))