from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.views.generic import View


from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from django.template import RequestContext

import datetime

class StudyIndex(View):
    def get(self,request):
        template = loader.get_template('study/index.html')
        context = {}
        return HttpResponse(template.render(context,request))
