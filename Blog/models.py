import datetime

from django.db import models
from django.utils import timezone

class Tag(models.Model):
    word = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.word

class BlogPost(models.Model):
    title = models.CharField(max_length=200,unique=True)
    body = models.TextField()
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag',blank=True)
    slug = models.SlugField(max_length=200, unique=True,allow_unicode=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    commenter = models.CharField(max_length=40)
    comment = models.TextField()
    postdate = models.DateTimeField(auto_now_add=True)
    blogpost = models.ForeignKey('BlogPost')

    def __str__(self):
        return self.commenter+ ' on '+ self.blogpost.title
