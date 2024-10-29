from django import template
from django.forms import BoundField


register = template.Library()

# @register.filter(name='addclass')
# def addclass(value, arg):
#     return value.as_widget(attrs={'class': arg})

# @register.filter(name='addid')
# def addid(value, arg):
#     return value.as_widget(attrs={'id': arg})


@register.filter(name='addclass')
def addclass(value, arg):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={'class': arg})
    return value

@register.filter(name='addid')
def addid(value, arg):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={'id': arg})
    return value

@register.filter(name='addtype')
def addtype(value, arg):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={'type': arg})
    return value

@register.filter(name='addstyle')
def addstyle(value, arg):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={'style': "height: 100px"})
    return value