from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from article.models import Article
from myadmin.serializers.article import ArticleSimpleSerializer


class AdminArticleSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ArticleSimpleSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = Article.objects.filter(title__contains=keyword).order_by('-create_time')
        else:
            queryset = Article.objects.all().order_by('-create_time')
        return queryset