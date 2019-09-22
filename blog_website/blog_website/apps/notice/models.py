from django.db import models

# Create your models here.
from blog_website.utils.models import BaseModel
from user.models import User


class Notice(BaseModel):
    """公告模型类"""
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name='公告标题', help_text='不能超过20个字')
    content = models.CharField(max_length=500, verbose_name='公告内容', help_text='不能超过500个字')
    is_up = models.BooleanField(default=False, verbose_name='是否置顶')
    read_count = models.IntegerField(default=0, verbose_name='阅读数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')

    class Meta:
        db_table = 'notice'
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
