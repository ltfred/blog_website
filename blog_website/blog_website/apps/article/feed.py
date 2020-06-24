from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from .models import Article


class BlogFeed(Feed):
    # 标题
    title = 'Fred的个人网站'
    # 描述
    description = '分享一些知识'
    # 链接
    link = "/"

    def items(self):
        # 返回所有文章
        return Article.objects.all()

    def item_title(self, item):
        # 返回文章标题
        return item.title

    def item_description(self, item):
        # 返回文章内容
        return item.content[:30]

    def item_link(self, item):
        # 返回文章详情页的路由
        return reverse('article:article_detail', args=(item.id,))
