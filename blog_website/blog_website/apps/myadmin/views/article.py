from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from article.models import Article
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