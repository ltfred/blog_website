from django.contrib import admin

# Register your models here.
from comment import models


@admin.register(models.Message)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['name', 'email']