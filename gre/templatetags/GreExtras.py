from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='LowerIt')
def LowerIt(value):
    ''' Converts a string to all lowercase '''
    return value.lower()

@register.filter(name="get_short_def")
def get_short_def(info_dict):
    return info_dict['def'].short_def

@register.filter(name="get_long_def")
def get_long_def(info_dict):
    return info_dict['def'].long_def


@register.filter(name="get_sent_list")
def get_sent_list(info_dict):
    return info_dict['sentences'] 


@register.filter(name="get_sentence")
def get_sentence(one_sent_dict):
    return one_sent_dict['sentence']

@register.filter(name="get_url")
def get_url(one_sent_dict):
    return one_sent_dict['url']

