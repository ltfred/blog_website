# _*_coding:utf-8_*_
# author: ltfred
import xadmin
from links.models import Link


class LinkAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['name', 'is_recommend']


xadmin.site.register(Link, LinkAdmin)