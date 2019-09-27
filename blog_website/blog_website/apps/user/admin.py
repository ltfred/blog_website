from django.contrib import admin
from user import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass
