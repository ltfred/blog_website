from photo.models import PhotoCategory, Photo
from rest_framework import serializers


class PhotoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCategory
        fields = ('id', 'name', 'is_secret')


class PhotoSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(label='照片分类', read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'category', 'title', 'category_id', 'url')


class PhotosSimpleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(label='照片分类', read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'category', 'title', 'url')