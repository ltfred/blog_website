import xadmin
from .models import *


class ArticleAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'author', 'category1', 'category2']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'category1':
            kwargs['queryset'] = ArticleCategory.objects.filter(parent__isnull=True)
        if db_field.name == 'category2':
            kwargs['queryset'] = ArticleCategory.objects.filter(parent__isnull=False)
        return super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class ArticleCategoryAdmin(object):
    ordering = ('-create_time',)
    list_display = ['name', 'parent']


class LabelAdmin(object):
    ordering = ('-create_time',)
    list_display = ['name']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(ArticleCategory, ArticleCategoryAdmin)
xadmin.site.register(Label, LabelAdmin)
