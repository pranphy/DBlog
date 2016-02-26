import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class News(models.Model):
    Title = models.CharField(max_length=300)
    Date = models.DateTimeField('Date Posted')
    Place = models.CharField(max_length=50)
    Source = models.CharField(max_length=100)
    NewsText = models.TextField()

    def __str__(self):
        return self.Title
