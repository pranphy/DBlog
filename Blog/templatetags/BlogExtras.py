from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='LowerIt')
def LowerIt(value):
    ''' Converts a string to all lowercase '''
    return value.lower()

@register.filter
@stringfilter
def Shorten(value,length):
    return value[0:length]

