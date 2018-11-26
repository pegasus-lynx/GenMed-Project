from django import template

register = template.Library()

@register.filter
def get(dict,key):
    return dict[key]

@register.filter
def getcity(dict,key):
    return dict[key][0][1]