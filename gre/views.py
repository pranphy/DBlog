#View for the gre app in my blog
import os
import requests
import random
import datetime
import json
import logging

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

from django.template import RequestContext
from django.template import loader

from .models import Tag 
from .models import Vocab 
from .models import VcVocab
from .models import VcSentence

from .error import NoInternet
from .error import NoSentenceInJson 
from .error import NoWordInInternet


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
    #should be deprecated in near future
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
    #class WordDefs () should be deprecated


    def allwords(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(BASE_DIR+'/gre/static/media/default.txt') as wordlist:
            for OneWord in wordlist:
                word = OneWord.strip()
                word.replace('\n','')
                yield word

    def fetch_from_list(self,wordlist):
        for word in wordlist.split(','):
            yield word
    

    def get_local_def(self,localvocab):
        short_def = localvocab.short_def
        long_def = localvocab.long_def
        meaning = localvocab.meaning
        word_info = {}
        word_info['def'] = self.WordDefs(short_def,long_def)
        word_info['meaning'] = meaning

        return word_info

    def get_local_sentences(self,localvocab):
        sent_obj_list =  VcSentence.objects.filter(vocab=localvocab)
        example_list = []
        for sentence_obj in sent_obj_list:
            sent_info = {}
            sent_info['sentence'] = sentence_obj.sentence
            sent_info['url'] = sentence_obj.url
            example_list.append(sent_info)

        return example_list

    def get_online_sentences(self,word,vocabobj):
        logging.info(' I am trying to find sentences online for word {}'.format(word))
        logging.info('type of vcvocab is \n {} \n'.format(type(vocabobj)))
        url = "https://corpus.vocabulary.com/api/1.0/examples.json?query="+word+"&maxResults=5"

        # See if thre is internet connection 
        try :
            sent_page = urlopen(url)
            soup = BeautifulSoup(sent_page)
            jsn = ''
            try:
                jsn = str(soup.select('body p')[0].string)
            except IndexError as e:
                jsn = str(soup)

            sent_dict = json.loads(jsn)
            try:
                vocabobj.save()
                example_list= [] 
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
                    VcSentence_obj.save()
                #end for
                return  example_list
            except KeyError as e:
                logging.info(' Error found {}'.format(str(e)))
                logging.info(' No sentences for word {} found '.format(word))
                raise NoSentenceInJson

        # Since there is no internet connection
        except URLError as e:
            raise NoInternet

        
    def get_online_vocab(self,word):
        logging.info('Trying to search the word {} online'.format(word))
        vocurl = "http://vocabulary.com/dictionary/"+word
        # Check if internet connection is online
        try:
            #get vocab info from this page 
            voc_page = urlopen(vocurl)
            soup = BeautifulSoup(voc_page)

            shortdef = soup.select('.definitionsContainer .main .section p.short')[0]
            longdef = soup.select('.definitionsContainer .main .section p.long')[0]
            #logging.info('Type of shortdef is {} and str(shortdef) is {}'.format(type(shortdef),str(shortdef)))

            VcVocab_obj = VcVocab(word=word, meaning = 'dummy', short_def = str(shortdef), long_def = str(longdef))
            logging.info(' The word {} is found online '.format(word))
            return VcVocab_obj
        except URLError as e:
            logging.error(' There is no internet connection ')
            raise NoInternet()
        except IndexError as e:
            logging.info(' There is no such word in internet connection ')
            raise NoWordInInternet()

    def get(self,request):
        logging.info(' Bravoo :: GET ')
        wordlist = request.GET.get('wordlist')
        word_generator = self.allwords()
        if wordlist:
            logging.info('Wordlist is not empty ')
            word_generator = self.fetch_from_list(wordlist)

        else:
            logging.info('Wordlist is empty ')

        logging.info('Wordlist is {}'.format(wordlist))
        logging.info(" ==========================================")
        logging.info(" I got a request to this file")
        template = loader.get_template('gre/test.html')
        worddef = {}
        i = 0
        for word in word_generator: 
            logging.info(' Got word {}'.format(word))
            i += 1
            word_info  = {}
            
            #Try to find the word out in local Database
            try:
                logging.info('Trying to find the  word {} exists in local '.format(word))
                localvocab = VcVocab.objects.get(word=word)
                logging.info(' The word {} exists in local vocab '.format(word))
                word_info['def'] =  self.WordDefs(localvocab.short_def,localvocab.long_def)
                word_info['meaning'] = localvocab.meaning

                #fetch sentences from loca vocab
                word_info['sentences'] = self.get_local_sentences(localvocab)

                
            # If the object is not in local database try to fetch from the internet
            except ObjectDoesNotExist as e:
                logging.info(' info or sentence for : {} doesnt exist in local '.format(word))
                try:
                    VcVocab_obj = self.get_online_vocab(word)

                    word_info['def'] = self.WordDefs(VcVocab_obj.short_def,VcVocab_obj.long_def)
                    word_info['meaning'] = VcVocab_obj.meaning

                    try:
                        word_info['sentences'] = self.get_online_sentences(word,VcVocab_obj)
                        logging.info(word_info['sentences'])
                    except NoSentenceInJson:
                        word_info['sentences'] = [{'sentence':'no sentence in json','url':'#'}]
                    except NoInternet:
                        word_info['sentences'] = [{'sentence':'no internet ','url':'#'}]
                #Can't fetch vocab object
                except NoInternet:
                    word_info['def'] = self.WordDefs('No internet','NoInternet')
                    word_info['meaning'] = 'No Internet '
                    word_info['sentences'] = [{'sentence':'no internet ','url':'#'}]
                except NoWordInInternet:
                    word_info['def'] = self.WordDefs('No word in internet','No word in Internet')
                    word_info['meaning'] = 'No such word Internet '
                    word_info['sentences'] = [{'sentence':'no such word in internet ','url':'#'}]
                #handled word from internet completely
            #handeled word from local or internet completely
            worddef[word] =  word_info
        #endfor interated for each word
        context = { 
            'worddef':worddef,
            'count':i,
        }
        return HttpResponse(template.render(context,request))
    def post(self,request):
        wordlist = request.POST.get('wordlist')
        logging.info('POST::Got words {}'.format(wordlist))
        return HttpResponseRedirect('/gre/test/')

