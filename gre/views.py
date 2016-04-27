#View for the gre app in my blog
import os
import requests
import random
import datetime
import json
import logging

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
from .models import VcVocab
from .models import VcSentence


logging.basicConfig(filename="NewLog.log",level=logging.DEBUG)

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
    
    def get_local_vocab(self,word):
        try:
            logging.info(' Testing if the word {} is in local vocab'.format(word))
            localvocab = VcVocab.objects.get(word=word)
            logging.info(' The word {} is in local vocab'.format(word))
            return localvocab
        except:
            logging.info('The word {} is not in local vocab'.format(word))
            return False

    def get_local_def(self,localvocab):
        short_def = localvocab.short_def
        long_def = localvocab.long_def
        meaning = localvocab.meaning
        word_info = {}
        word_info['def'] = self.WordDefs(short_def,long_def)
        word_info['meaning'] = meaning

        return word_info

    def get_local_sentences(self,localvocab):
        sent_obj_list =  VcSentence.objects.get(vocab=localvocab)
        example_list = []
        for sentence_obj in sent_obj_list:
            sent_info = {}
            sent_info['sentence'] = sentence_obj.sentence
            sent_info['url'] = sentence_obj.url
            example_list.append(sent_info)

        return example_list

    def get_online_sentences(self,word,vocabobj):
        logging.info(' I am trying to find sentences online for word {}'.format(word))
        url = "https://corpus.vocabulary.com/api/1.0/examples.json?query="+word+"&maxResults=5"
        soup = BeautifulSoup(urlopen(url),"lxml")
        jsn = ''
        try:
            jsn = str(soup.select('body p')[0].string)
        except:
            jsn = str(soup)

        sent_dict = json.loads(jsn)
        example_list= [] 
        try:
            try:
                logging.info('Tyring to save vocab object for word {}'.format(word))
                vocabobj.save();
                logging.info(' --- Success ')
            except:
                logging.info(' ---------FAILED to save ')

            for obj in sent_dict['result']['sentences']:
                sent_info = {}
                sent_info['sentence'] = obj['sentence']
                sent_info['url'] = obj['volume']['locator']
                example_list.append(sent_info)
                VcSentence_obj = VcSentence(
                    sentence = obj['sentence'],
                    url = sent_info['url'],
                    vocab = vocabobj
                )
                try:
                    logging.info(' Tryig to save sentences  for {} '.format(word))
                    VcSentence_obj.save()
                    logging.info(' ----failed ')
                except:
                    logging.info(' ------------------Success ')
        except:
            logging.info(' No sentences for word {} found '.foramt(word))
            sent_info = {}
            sent_info['sentence'] = 'Not found'
            sent_info['url'] = "#"
            example_list.append(sent_info)


        return example_list

    def get_online_vocabobj(self,word):
        logging.info('Trying to search the word {} online'.format(word))
        url = "http://vocabulary.com/dictionary/"+word
        soup = BeautifulSoup(urlopen(url),"lxml")
        try:

            shortdef = soup.select('.definitionsContainer .main .section p.short')[0]
            longdef = soup.select('.definitionsContainer .main .section p.long')[0]
            VcVocab_obj = VcVocab(
                word=word,
                meaning = 'dummy',
                short_def = shortdef,
                long_def = longdef
            )
            logging.info(' The word {} is found online '.format(word))
            return  VcVocab_obj
        except:
            logging.info(' The word {} is not found online '.format(word))
            return False

    def get(self,request):
        logging.info(" ==========================================")
        logging.info(" I got a request to this file")
        template = loader.get_template('gre/test.html')
        worddef = {}
        i = 0
        for word in self.allwords():
            logging.info(' Got word {}'.format(word))
            i += 1
            word_info  = {}
            localvocab = self.get_local_vocab(word)
            logging.info(' Returned back from local vocab for word {}'.format(word))
            if localvocab:
                logging.info(' word :',word,' exists in local ')
                word_info['def'] = localvocab['def']
                word_info['meaning'] = localvocab['meaning']
                word_info['sentences'] = get_local_sentences(localvocab)
            else:
                logging.info(' word : {} doesnt exist in local '.format(word))
                VcVocab_obj = self.get_online_vocabobj(word)
                if VcVocab_obj != False:
                    logging.info(' Fetched the word info for {} from internet '.format(word))
                    VcSentence_obj = self.get_online_sentences(word,VcVocab_obj)

                    word_info['def'] = self.WordDefs(VcVocab_obj.short_def,VcVocab_obj.long_def)
                    word_info['meaning'] = VcVocab_obj.meaning
                    word_info['sentences'] = self.get_online_sentences(word,VcVocab_obj)
                else:
                    word_info['def'] = self.WordDefs('Not found','Not Found')
                    word_info['meaning'] = 'Not found '
                    word_info['sentences']=[]

            worddef[word] =  word_info

        context = { 
            'worddef':worddef,
            'count':i,
        }
        return HttpResponse(template.render(context,request))
