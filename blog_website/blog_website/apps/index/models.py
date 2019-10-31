from django.db import models

# Create your models here.
from blog_website.utils.models import BaseModel


class Carousel(BaseModel):
    image_url = models.CharField(max_length=200, verbose_name='图片地址')
    url = models.CharField(max_length=200, verbose_name='指向地址')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        db_table = 'carousel'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
