from rest_framework import serializers
from article.models import Article, ArticleCategory


class ArticleSimpleSerializer(serializers.ModelSerializer):
    category1 = serializers.StringRelatedField(label='一级分类', read_only=True)
    category2 = serializers.StringRelatedField(label='二级分类', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'category1', 'category2', 'read_count', 'like_count')


class ArticleSerializer(serializers.ModelSerializer):
    category1_id = serializers.PrimaryKeyRelatedField(label='一级分类', read_only=True)
    category2_id = serializers.PrimaryKeyRelatedField(label='一级分类', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'author_id', 'author','index_image', 'title', 'category1_id', 'category2_id',
                  'content', 'describe', 'read_count', 'like_count', 'is_top', 'category1', 'category2',
                  'labels')


class ArticleCategorySimpleSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(label='上级分类名称', read_only=True)

    class Meta:
        model = ArticleCategory
        fields = ('id', 'name', 'parent')