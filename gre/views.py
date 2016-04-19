#View for the gre app in my blog
import os
import requests
import random
import datetime
import json

from urllib.request import urlopen
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import View

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from django.template import RequestContext
from django.template import loader

from .models import Tag 
from .models import Vocab 


class GreIndex(View):
    def get(self,request):
        allword = list(Vocab.objects.all())
        random.shuffle(allword)

        template = loader.get_template('gre/index.html')
        Repeat = [1,2]
        context   = {
            'Repeat' : Repeat,
            'allword' : allword,
        }
        return HttpResponse(template.render(context,request))

class GreMeaning(View):
    def get(self,request,pword):
        currentword = get_object_or_404(Vocab,word = pword) 
        template = loader.get_template('gre/meaning.html')
        context = {
            'pword':pword,
            'currentword': currentword
        }
        return HttpResponse(template.render(context,request))

class GreTag(View):
    def get(self,request,ptag):
        tagids = get_list_or_404(Tag,tagname__contains = ptag)
        tagwords = get_list_or_404(Vocab,category__in = tagids)
        template = loader.get_template('gre/tags.html')
        context = { 
            'tagwords':tagwords,
            'tag' : ptag
        }
        return HttpResponse(template.render(context,request))

class GreAllTag(View):
    def get(self,request):
        template = loader.get_template('gre/alltags.html')
        alltags = Tag.objects.all()
        tagvocab = {}
        for tag in alltags:
            allwords = Vocab.objects.filter(category = tag.id)
            tagvocab[tag.tagname] = allwords

        context = {
            'tagvocab' : tagvocab
        }
        return HttpResponse(template.render(context, request))

class TestScrap(View):
    class WordDefs():
        short_def = ''
        long_def = ''
        def __init__(self,sdef,ldef):
            self.short_def = sdef
            self.long_def = ldef

        def set_short_def(self,sdef):
            self.short_def = sdef

        def set_long_def(self,ldef):
            self.long_def = ldef




    def allwords(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(BASE_DIR+'/gre/static/media/default.txt') as wordlist:
            for OneWord in wordlist:
                Word = OneWord.strip()
                Word.replace('\n','')
                yield Word
    
    def get_sentences(self,word):
        url = "https://corpus.vocabulary.com/api/1.0/examples.json?query="+word+"&maxResults=5"
        soup = BeautifulSoup(urlopen(url))
        #jsn = str(soup)
        jsn = str(soup.select('body p')[0].string)
        sent_dict = json.loads(jsn)
        example_list= [] 
        for obj in sent_dict['result']['sentences']:
            sent_info = {}
            sent_info['sentence'] = obj['sentence']
            sent_info['url'] = obj['volume']['locator']
            example_list.append(sent_info)

        return example_list

    def get_def(self,word):
        url = "http://vocabulary.com/dictionary/"+word
        soup = BeautifulSoup(urlopen(url))
        try:
            shortdef = soup.select('.definitionsContainer .main .section p.short')[0]
            longdef = soup.select('.definitionsContainer .main .section p.long')[0]
            return self.WordDefs(str(shortdef),str(longdef))
        except:
            return self.WordDefs('not fount','not found')

    def get(self,request):
        template = loader.get_template('gre/test.html')
        worddef = {}
        i = 0
        for word in self.allwords():
            i += 1
            word_info  = {}
            word_info['def'] = self.get_def(word)
            word_info['sentences'] = self.get_sentences(word)
            worddef[word] =  word_info

        context = { 
            'worddef':worddef,
            'count':i,
        }
        return HttpResponse(template.render(context,request))


        
