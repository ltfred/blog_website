from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    """用户模型类"""
    profession = models.CharField(max_length=10, verbose_name='职业')
    address = models.CharField(max_length=10, verbose_name='地址')
    avatar_url = models.CharField(max_length=200, null=True, verbose_name='用户头像路径')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
    