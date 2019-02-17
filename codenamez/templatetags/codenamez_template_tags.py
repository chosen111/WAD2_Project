from django import template
from django.urls import reverse

register = template.Library()

@register.inclusion_tag('codenamez/tags/logo.html')
def createLogoBySize(size="big"):
    return { 'size': size }

@register.inclusion_tag('codenamez/tags/button.html')
def createButton(id=None, text="", href=None):
    link = None
    try:
        link = reverse(href)
    except:
        link = href

    return { 'id': id, 'text': text, 'href': link }