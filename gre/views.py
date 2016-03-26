from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from django.template import RequestContext

import datetime

from .models import Tag 
from .models import Vocab 


def index(request):
    allword= Vocab.objects.all()
    template = loader.get_template('gre/index.html')
    Repeat = [1,2]

    context   = {
        'Repeat' : Repeat,
        'allword' : allword,
    }
    return HttpResponse(template.render(context,request))

def detail(request,pword):
    currentword = get_object_or_404(Vocab,word=pword) 
    template = loader.get_template('gre/details.html')
    context = {
        'pword':pword,
        'currentword': currentword
    }
    return HttpResponse(template.render(context,request))
