from django import template

register = template.Library()

# This tag is used to get the value from a  key,value pair from a dictionary
# by the help of key as filter . 
@register.filter
def get(dict,key):
    return dict[key]

# This tag is used to get the city from a  key,value pair from a dictionary
# by the help of key as filter having a customized list having the city. 
@register.filter
def getcity(dict,key):
    return dict[key][2]