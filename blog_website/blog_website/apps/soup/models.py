from django.db import models


# Create your models here.

class Soup(models.Model):
    """鸡汤"""
    content = models.CharField(max_length=50, verbose_name='内容')

    class Meta:
        db_table = 'soup'
        verbose_name = '鸡汤'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content