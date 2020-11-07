import xadmin
from .models import *


class PhotoCategoryAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['name', 'is_secret']


class PhotoGroupAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'category']


class PhotoAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'group']


xadmin.site.register(PhotoCategory, PhotoCategoryAdmin)
xadmin.site.register(Photo, PhotoAdmin)
xadmin.site.register(PhotoGroup, PhotoGroupAdmin)
