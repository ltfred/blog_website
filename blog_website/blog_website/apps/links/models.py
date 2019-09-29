from django.db import models

# Create your models here.
from blog_website.utils.models import BaseModel


class Link(BaseModel):
    """链接模型类"""
    name = models.CharField(max_length=20, verbose_name='名字')
    url = models.CharField(max_length=100, verbose_name='链接', help_text='必须以http/https开头')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')

    class Meta:
        db_table = 'link'
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name