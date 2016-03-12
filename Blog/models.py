import datetime

from django.db import models
from django.utils import timezone

class News(models.Model):
    Title = models.CharField(max_length=300)
    Date = models.DateTimeField('Date Posted')
    Place = models.CharField(max_length=50)
    Source = models.CharField(max_length=100)
    NewsText = models.TextField()

    def __str__(self):
        return self.Title

class BlogPost(models.Model):
    Title = models.CharField(max_length=300)
    PostDate = models.DateTimeField('PostDate')
    PublishDate = models.DateTimeField('PublishDate')
    Likes = models.PositiveSmallIntegerField()
    Contents = models.TextField();
    Slug = models.SlugField()

    
    def __str__(self):
        return self.Title

class NavigationItems(models.Model):
    DisplayName = models.CharField(max_length=50)
    GlyphIconClass = models.CharField(max_length=20)
    Link = models.CharField(max_length=50)

    def __str__(self):
        return self.DisplayName
