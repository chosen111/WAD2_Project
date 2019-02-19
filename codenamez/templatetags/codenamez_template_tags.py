from django import template
from django.urls import reverse

register = template.Library()

@register.inclusion_tag('codenamez/tags/logo.html')
def createLogoBySize(size="big"):
    return { 'size': size }

@register.inclusion_tag('codenamez/tags/button.html')
def createButton(id, text, href=None, isAnchor=False):
    link = None
    try:
        link = reverse(href)
    except:
        link = href

    return { 'id': id, 'text': text, 'href': link, 'isAnchor': isAnchor }

@register.inclusion_tag('codenamez/tags/user.html')
def user(user):
    return { 'username': user.username, 'avatar': user.userprofile.avatar, 'is_staff': user.is_staff }