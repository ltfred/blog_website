from django.db import models

# Create your models here.
from blog_website.utils.models import BaseModel
from user.models import User


class ArticleCategory(BaseModel):
    """文章分类"""
    name = models.CharField(max_length=10, verbose_name='名称')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subs',
                               on_delete=models.CASCADE, verbose_name='父类别')

    class Meta:
        db_table = 'article_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    """文章"""
    author = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    category1 = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT,
                                  related_name='cat1', verbose_name='一级分类')
    category2 = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT,
                                  related_name='cat2', verbose_name='二级分类')
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    index_image = models.CharField(max_length=300, null=True, verbose_name='文章主图')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    describe = models.TextField(default='', verbose_name='文章描述')

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
