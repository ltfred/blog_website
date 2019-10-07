from django.db import models

# Create your models here.
from blog_website.utils.models import BaseModel


class Message(BaseModel):
    name = models.CharField(max_length=10, verbose_name='留言人')
    email = models.CharField(max_length=50, verbose_name='邮箱')
    content= models.TextField(verbose_name='留言内容')

    class Meta:
        db_table = 'message'
        verbose_name = '留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name