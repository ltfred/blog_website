from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    """用户模型类"""
    webname = models.CharField(max_length=20, verbose_name='网名', default='')
    profession = models.CharField(max_length=30, verbose_name='职业')
    address = models.CharField(max_length=10, verbose_name='地址')
    avatar_url = models.CharField(max_length=200, null=True, verbose_name='用户头像路径')
    bio = models.CharField(max_length=200, default='', verbose_name='个人简介')
    soliloquy = models.TextField(default='', verbose_name='独白')


    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
