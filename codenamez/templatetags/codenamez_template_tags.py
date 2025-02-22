from datetime import datetime

from django import template
from django.urls import reverse
from codenamez.models import UserProfile

register = template.Library()

@register.simple_tag
def ftime(timestamp):
    if timestamp:
        return datetime.utcfromtimestamp(timestamp).strftime('%d %b %Y at %H:%M:%S')
    return 'No'

@register.inclusion_tag('codenamez/tags/logo.html')
def createLogoBySize(size="big"):
    return { 'size': size }

@register.inclusion_tag('codenamez/tags/button.html')
def createButton(id, text, href=None, args=None, isAnchor=False):
    try:
        if args is None:
            href = reverse(href) 
        else:
            href = reverse(href, args=[args])             
    except:
        pass

    return { 'id': id, 'text': text, 'href': href, 'isAnchor': isAnchor }

@register.inclusion_tag('codenamez/tags/user.html')
def user(user):
    try: 
        avatar = user.userprofile.avatar
    except UserProfile.DoesNotExist: 
        avatar = None
    return { 'id': user.id, 'username': user.username, 'avatar': avatar, 'is_staff': user.is_staff }

@register.inclusion_tag('codenamez/tags/stats-row.html')
def addStatsRow(id="placeholder", label="Placeholder", value="Placeholder", customClass=None):
    return { 'id': id, 'label': label, 'value': value, 'customClass': customClass }

@register.inclusion_tag('codenamez/tags/error.html')
def showError(message="null"):
    return { 'message': message }

@register.inclusion_tag('codenamez/tags/loading.html')
def showLoading(text=None):
    return { 'text': text }