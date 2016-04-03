from django.db import models
import datetime

from django.utils import timezone

class Source(models.Model):
    class Type(models.Model):
        stype = models.CharField(max_length=20,unique=True)

        def __str__(self):
            return self.stype;

    name =  models.CharField(max_length=20,unique=True)
    type = models.ManyToManyField('Type', blank=False)

    def __str__(self):
        return self.name



class Tag(models.Model):
    tagname = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.tagname

class Vocab(models.Model):
    word = models.CharField(max_length=25,unique=True)
    meaning = models.CharField(max_length=250)
    sentences = models.TextField();
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField('Tag',blank=False)
    source = models.ManyToManyField('Source',blank=False)
    synonym = models.ManyToManyField('Vocab',  blank=True, related_name="%(app_label)s_%(class)s_related_synonym")
    antonym = models.ManyToManyField('Vocab',  blank=True, related_name="%(app_label)s_%(class)s_related_antonym")
    seealso = models.ManyToManyField('Vocab',  blank=True, related_name="%(app_label)s_%(class)s_related_see_also" )

    def __str__(self):
        return self.word