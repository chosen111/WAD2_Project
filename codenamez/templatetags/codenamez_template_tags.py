from django import template
from django.urls import reverse
from codenamez.models import UserProfile

register = template.Library()

@register.inclusion_tag('codenamez/tags/logo.html')
def createLogoBySize(size="big"):
    return { 'size': size }

@register.inclusion_tag('codenamez/tags/button.html')
def createButton(id, text, href=None, isAnchor=False):
    try:
        link = reverse(href)
    except:
        link = href

    return { 'id': id, 'text': text, 'href': link, 'isAnchor': isAnchor }

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