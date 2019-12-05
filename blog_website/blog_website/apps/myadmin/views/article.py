from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from article.models import Article, ArticleCategory
from myadmin.serializers.article import ArticleSimpleSerializer
from user.models import User


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


class AdminAuthorSimpleView(APIView):
    permission_classes = [IsAdminUser]
    """作者信息"""

    def get(self, request):
        users = User.objects.filter(is_staff=True)
        lists = [{'id': user.id, 'username': user.username} for user in users]
        return Response({'code': 200, 'lists': lists})


class AdminArticleCategory1View(APIView):
    permission_classes = [IsAdminUser]
    """一级分类"""

    def get(self, request):
        categories1 = ArticleCategory.objects.filter(parent__isnull=True)
        lists = [{'id': category1.id, 'name': category1.name} for category1 in categories1]
        return Response(lists)


class AdminArticleCategory2View(APIView):
    permission_classes = [IsAdminUser]
    """二级分类"""

    def get(self, request, category_id):
        category = ArticleCategory.objects.get(id=category_id)
        categories2 = ArticleCategory.objects.filter(parent_id=category_id)
        subs = [{'id': category2.id, 'name': category2.name} for category2 in categories2]
        return Response({'id': category.id, 'subs': subs})