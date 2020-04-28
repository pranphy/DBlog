#View for the gre app in my blog
import os
import re
import requests
import random
import datetime
import json
import logging

import plotly  as  ply


from urllib.request import urlopen
from urllib.error import URLError

from bs4 import BeautifulSoup

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import View

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from django.template import RequestContext,Context, loader

from .models import Tag, Vocab, VcVocab, VcSentence

from .error import NoInternet, NoSentenceInJson,NoWordInInternet

logging.basicConfig(filename='NewLog.log', level=logging.DEBUG,
                    format='[%(asctime)s.%(msecs)d] [%(levelname)s] : %(message)s', 
                    #format='[%(asctime)s.%(msecs)d %(levelname)s] %(module)s - %(funcName)s: %(message)s', 
                    datefmt="%Y-%m-%d %H:%M:%S")
class VisonIndex(View):
    def get(self,request):

        template = loader.get_template('vison/index.html')
        allword = ['hera','na','sahidharulai']
        Repeat = [1,2]
        context   = {
            'Repeat' : Repeat,
            'allword' : allword,
        }
        return HttpResponse(template.render(context,request))


class VisonGraph(View):
    def get(self, request):
        template = loader.get_template('vison/graph.html')
        #context = super(Graph, self).get_context_data(**kwargs)

        trace0 = ply.graph_objs.Scatter(
            x=[1, 2, 3, 4],
            y=[10, 15, 13, 17]
        )
        trace1 = ply.graph_objs.Scatter(
            x=[1, 2, 3, 4],
            y=[16, 5, 11, 9]
        )
        data = [trace0, trace1]

        div = ply.offline.plot(data, auto_open=False, output_type='div',config={"displayModeBar": False})
        div2 = ply.offline.plot([trace1], auto_open=False, output_type='div',config={"displayModeBar": False})

        context = {
                'allgraphs' : [div,div2]
                }

        return HttpResponse(template.render(context,request))
        #return context



