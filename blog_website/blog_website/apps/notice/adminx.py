# _*_coding:utf-8_*_
# author: ltfred
import xadmin
from .models import Notice

class NoticeAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['user', 'title']


xadmin.site.register(Notice, NoticeAdmin)