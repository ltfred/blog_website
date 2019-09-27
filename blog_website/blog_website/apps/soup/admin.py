from django.contrib import admin

# Register your models here.
from soup import models
from soup.models import Soup


@admin.register(models.Soup)
class SoupAdmin(admin.ModelAdmin):
    pass
