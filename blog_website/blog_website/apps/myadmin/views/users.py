from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from myadmin.serializers.users import AdminAuthSerializer, UserSerializer
from user.models import User


class AdminAuthorizeView(APIView):

    def post(self, request):
        serializer = AdminAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminUserView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = User.objects.filter(Q(username__contains=keyword) | Q(webname__contains=keyword))
        else:
            queryset = User.objects.all()
        return queryset
