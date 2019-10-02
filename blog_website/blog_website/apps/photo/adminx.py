import xadmin
from .models import *


class PhotoCategoryAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)


class PhotoAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'category']


xadmin.site.register(PhotoCategory, PhotoCategoryAdmin)
xadmin.site.register(Photo, PhotoAdmin)
