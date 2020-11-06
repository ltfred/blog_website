from django.db import models
from django.utils.translation import ugettext_lazy as _

from blog_website.utils.constants import Const
from blog_website.utils.models import BaseModel


class PhotoCategory(BaseModel):
    """照片分类"""
    name = models.CharField(max_length=Const.LEN.TITLE, verbose_name='相册类名', help_text='不超过50个字')
    is_secret = models.BooleanField(default=False, verbose_name='是否秘密的')

    class Meta:
        db_table = 'photo_category'
        verbose_name = '相册类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PhotoGroup(BaseModel):
    """照片组"""
    title = models.CharField(max_length=Const.LEN.TITLE, verbose_name="组名")
    index_image = models.URLField(max_length=Const.LEN.URL, verbose_name="主图url", help_text="https或http开头")
    category = models.ForeignKey(PhotoCategory, on_delete=models.CASCADE, related_name="groups")

    class Meta:
        db_table = 'photo_group'
        verbose_name = '相册组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Photo(BaseModel):
    """照片"""

    title = models.CharField(max_length=Const.LEN.TITLE, verbose_name='照片标题', help_text=_('No more than 50 characters'))
    url = models.CharField(max_length=Const.LEN.URL, verbose_name='照片地址', null=True)
    thumbnail_url = models.URLField(max_length=Const.LEN.URL, null=True, verbose_name="缩略图")
    group = models.ForeignKey(PhotoGroup, null=True, on_delete=models.CASCADE, related_name="photos")

    class Meta:
        db_table = 'photos'
        verbose_name = '照片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
