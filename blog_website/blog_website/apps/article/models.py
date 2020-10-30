from ckeditor.fields import RichTextField
from django.db import models
from blog_website.utils.models import BaseModel
from user.models import User


class ArticleCategory(BaseModel):
    """文章分类"""
    name = models.CharField(max_length=20, verbose_name='名称', help_text='不超过20个字')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subs',
                               on_delete=models.CASCADE, verbose_name='父类别')
    describe = models.CharField(max_length=100, default='', verbose_name='类别描述', help_text='不超过100个字')
    image_url = models.CharField(max_length=1000, null=True, verbose_name='类别图片')

    class Meta:
        db_table = 'article_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_articles(self):
        # 判断是否为一级分类
        if self.parent is None:
            # 获取一级下的所有文章
            articles = Article.objects.filter(category1=self).order_by('-create_time')
        else:
            # 为二级分类，二级类下的所有文章
            articles = Article.objects.filter(category2=self).order_by('-create_time')
        category_article_count = articles.count()
        return articles, category_article_count


class Article(BaseModel):
    """文章"""
    author = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(max_length=50, verbose_name='标题', help_text='b不超过50字')
    content = RichTextField(verbose_name='内容')
    category1 = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT,
                                  related_name='cat1', verbose_name='一级分类')
    category2 = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT,
                                  related_name='cat2', verbose_name='二级分类')
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    index_image = models.CharField(max_length=1000, null=True, verbose_name='文章主图')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    describe = models.TextField(default='', verbose_name='文章描述', help_text='用于列表页展示文章简介')
    labels = models.ManyToManyField('Label', verbose_name='文章标签')

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_next_article(self):
        next_article = Article.objects.filter(
            id__gt=self.id, category2=self.category2).only('id', 'title').first()
        return next_article

    def get_pre_article(self):
        pre_article = Article.objects.filter(
            id__lt=self.id, category2=self.category2).only('id', 'title').order_by('-id').first()
        return pre_article

    def get_connected_article(self):
        articles = Article.objects.filter(category2=self.category2).exclude(id=self.id).only('id', 'title')[0:9]
        return articles


class Label(BaseModel):
    """文章标签"""
    name = models.CharField(max_length=20, verbose_name='文章标签', help_text='不超过20个字')

    class Meta:
        db_table = 'label'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_label_articles(self):
        articles = self.article_set.all().order_by('-create_time')
        article_count = articles.count()
        return articles, article_count
