from django.contrib import admin

# Register your models here.
from links import models
from links.models import Link


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['name', 'is_recommend']
