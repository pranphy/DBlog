import datetime
import os

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


    def handle_upload_file(self,rfile,receivedfilename):
        # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(BASE_DIR+'/static/uploads/' + receivedfilename,'wb+') as destination:
            for chunk in rfile.chunks():
                destination.write(chunk)


    def post(self,request):
        name = request.POST.get('commenter')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        form = TestForm(request.POST,request.FILES)
        receivedfile = request.FILES['uploadfile']
        receivedfilename = request.POST.get('filename')
        self.handle_upload_file(receivedfile,receivedfilename)
        return HttpResponseRedirect('/study/test/')


class MarkdownTest(View):
    def get(self,request):
        text = ''
        with open('study/markdown/Test.md') as testmd:
            text = testmd.read()

        context = {'mdtext' : text };
        template = loader.get_template('study/mdview.html')
        return HttpResponse(template.render(context,request))


