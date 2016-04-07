import datetime

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from django.template import RequestContext
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import View


from .forms import TestForm

import os

class StudyIndex(View):
    def get(self,request):
        template = loader.get_template('study/index.html')
        context = {}
        return HttpResponse(template.render(context,request))

class TestView(View):
    def get(self,request):
        template = loader.get_template('study/test.html')
        form = TestForm()
        context = {
            'form' : form,
        }
        return HttpResponse(template.render(context,request))


    def handle_upload_file(self,f):
        # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        with open(BASE_DIR+'/static/images/test','wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)


    def post(self,request):
        name = request.POST.get('commenter')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        form = TestForm(request.POST,request.FILES)
        receivedfile = request.FILES['uploadfile']
        self.handle_upload_file(receivedfile)
        return HttpResponseRedirect('/study/test/')


