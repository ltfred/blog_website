from django.contrib import admin

# Register your models here.
from photo import models


@admin.register(models.PhotoCategory)
class PhotoCategoryAdmin(admin.ModelAdmin):
    list_filter = ('create_time',)
    ordering = ('-create_time',)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'category']