import re

__author__ = 'Cynthia'

from django import template

register = template.Library()

@register.filter(name='youtube_embed')
def youtube_embed(value):

    # match = re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$', value)
    match = re.search(r'^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$', value)
    if match:
        embed_url = 'http://www.youtube.com/embed/%s' %(match.group(2))
        res = "<iframe width=\"760\" height=\"450\" src=\"%s\" frameborder=\"0\" allowfullscreen ></iframe>" %(embed_url)
        return res
    return ''