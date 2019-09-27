from django.contrib import admin

# Register your models here.
from notice import models


@admin.register(models.Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['user', 'title']
