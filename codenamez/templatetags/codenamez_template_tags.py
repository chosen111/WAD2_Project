from django import template

register = template.Library()

@register.inclusion_tag('codenamez/tags/logo.html')
def getLogoBySize(size="big"):
    return { 'size': size }