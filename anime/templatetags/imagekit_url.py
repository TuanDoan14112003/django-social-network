from django import template
from django.conf import settings
import os
register = template.Library()

@register.filter
def change_to_imagekit_url(value):
    return os.path.join(settings.IMAGEKIT_URL_ENDPOINT,value)




def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

url_target_blank = register.filter(url_target_blank, is_safe = True)
