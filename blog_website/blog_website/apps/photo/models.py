from django.db import models
from django.utils.translation import ugettext_lazy as _
from blog_website.utils.models import BaseModel


class PhotoCategory(BaseModel):
    """照片分类"""
    name = models.CharField(max_length=10, verbose_name='相册类名', help_text='不超过10个字')

    class Meta:
        db_table = 'photo_category'
        verbose_name = '相册类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Photo(BaseModel):
    """照片"""

    title = models.CharField(max_length=10, verbose_name='照片标题', help_text=_('No more than 10 characters'))
    url = models.CharField(max_length=1000, verbose_name='照片地址', null=True)
    category = models.ForeignKey(PhotoCategory, on_delete=models.PROTECT, verbose_name='照片类别', related_name='photos')

    class Meta:
        db_table = 'photos'
        verbose_name = '照片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title