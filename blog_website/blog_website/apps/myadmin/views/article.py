from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from article.models import Article, ArticleCategory, Label
from blog_website.utils.common import upload
from myadmin.serializers.article import ArticleSimpleSerializer, ArticleSerializer, ArticleCategorySimpleSerializer
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


class AdminLabelView(APIView):
    permission_classes = [IsAdminUser]
    """标签获取"""

    def get(self, request):
        labels = Label.objects.all()
        lists = [{'id': label.id, 'name': label.name} for label in labels]
        return Response({'code': 200, 'lists': lists})


# 文章修改，添加，删除
class AdminArticleView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_value_regex = '\d+'


class AdminArticleIndexImageView(APIView):
    permission_classes = [IsAdminUser]
    """文章主图添加"""

    def post(self, request):
        id = request.data.get('id')
        image = request.data.get('image')
        article = Article.objects.get(id=id)
        url = upload(image.name, image.read())
        article.index_image = url
        article.save()
        return Response(status=201)


class AdminArticleCategorySimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ArticleCategorySimpleSerializer
    queryset = ArticleCategory.objects.all().order_by('-create_time')


class AdminArticleCategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, category_id):
        name = request.data.get('name')
        parent_id = request.data.get('parent_id')
        describe = request.data.get('describe')
        category = ArticleCategory.objects.get(id=category_id)
        category.name = name
        category.parent_id = parent_id
        category.describe = describe
        category.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, category_id):
        category = ArticleCategory.objects.get(id=category_id)
        category.delete()
        return Response(status=204)

    def get(self, request, category_id):
        category = ArticleCategory.objects.get(id=category_id)
        return Response({
            'image_url': category.image_url, 'name': category.name,
            'parent_id': category.parent_id, 'describe': category.describe
        })


class AdminArticleCategory(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        name = request.data.get('name')
        parent_id = request.data.get('parent')
        describe = request.data.get('describe')
        if parent_id == 'undefined':
            ArticleCategory.objects.create(name=name, describe=describe)
        else:
            ArticleCategory.objects.create(name=name, parent_id=parent_id, describe=describe)
        return Response(status=status.HTTP_201_CREATED)


class AdminCategoryImageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        id = request.data.get('id')
        image = request.data.get('image')
        category = ArticleCategory.objects.get(id=id)
        url = upload(image.name, image.read())
        category.image_url = url
        category.save()
        return Response(status=status.HTTP_201_CREATED)