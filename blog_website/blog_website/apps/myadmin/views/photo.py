from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from blog_website.utils.common import upload
from myadmin.serializers.photo import PhotoCategorySerializer, PhotoSerializer, PhotosSimpleSerializer
from photo.models import PhotoCategory, Photo


class AdminPhotoCategoryView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = PhotoCategorySerializer
    queryset = PhotoCategory.objects.all().order_by('-create_time')


class AdminPhotoView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all().order_by('-create_time')


class AdminPhotoCategory(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        categories = PhotoCategory.objects.all()
        lists = [{'id': category.id, 'name': category.name} for category in categories]
        return Response(lists)


class AdminPhotoImageView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        id = request.data.get('id')
        image = request.data.get('photo')
        photo = Photo.objects.get(id=id)
        url = upload(image.name, image.read())
        photo.url = url
        photo.save()
        return Response(status=HTTP_201_CREATED)


class AdminPhotosSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PhotosSimpleSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = Photo.objects.filter(title__contains=keyword).order_by('-create_time')
        else:
            queryset = Photo.objects.all().order_by('-create_time')
        return queryset