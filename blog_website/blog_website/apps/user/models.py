from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    """用户模型类"""
    webname = models.CharField(max_length=20, verbose_name='网名', default='')
    profession = models.CharField(max_length=30, verbose_name='职业')
    address = models.CharField(max_length=10, verbose_name='地址')
    avatar_url = models.CharField(max_length=1000, null=True, verbose_name='用户头像路径')
    bio = models.CharField(max_length=300, default='', verbose_name='个人简介', help_text='不超过300字')
    soliloquy = models.TextField(default='', verbose_name='独白')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @staticmethod
    def get_profile():
        user = User.objects.filter(is_superuser=True).first()
        profile = dict()
        profile['webname'] = user.webname
        profile['profession'] = user.profession
        profile['address'] = user.address
        profile['email'] = user.email
        return profile