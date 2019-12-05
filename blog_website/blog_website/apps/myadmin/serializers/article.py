from rest_framework import serializers
from article.models import Article


class ArticleSimpleSerializer(serializers.ModelSerializer):
    category1 = serializers.StringRelatedField(label='一级分类', read_only=True)
    category2 = serializers.StringRelatedField(label='二级分类', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'category1', 'category2', 'read_count', 'like_count')