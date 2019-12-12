from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from myadmin.serializers.soup import SoupSerializer
from soup.models import Soup


class AdminSoupView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SoupSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = Soup.objects.filter(content__contains=keyword)
        else:
            queryset = Soup.objects.all()
        return queryset