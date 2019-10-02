import xadmin
from .models import *


class ArticleAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'author', 'category1', 'category2']


class ArticleCategoryAdmin(object):
    ordering = ('-create_time',)
    list_display = ['name', 'parent']


class LabelAdmin(object):
    ordering = ('-create_time',)
    list_display = ['name']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(ArticleCategory, ArticleCategoryAdmin)
xadmin.site.register(Label, LabelAdmin)
