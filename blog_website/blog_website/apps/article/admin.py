from django.contrib import admin

# Register your models here.
from article import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'author', 'category1', 'category2']


@admin.register(models.ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    ordering = ('-create_time',)
    list_display = ['name', 'parent']


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin):
    ordering = ('-create_time',)
    list_display = ['name']
