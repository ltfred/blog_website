import xadmin
from .models import *


class MessageAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['name', 'email']


xadmin.site.register(Message, MessageAdmin)
