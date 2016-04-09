import markdown

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='LowerIt')
def LowerIt(value):
    ''' Converts a string to all lowercase '''
    return value.lower()

@register.filter
@stringfilter
def shorten(value,length):
    return value[0:length]

@register.filter
@stringfilter
def markdownify(string):
    html = markdown.markdown(string)
    return html
