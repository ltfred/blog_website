from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from links.models import Link
from myadmin.serializers.link import LinkSerializer


class AdminLinkView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LinkSerializer
    queryset = Link.objects.all().order_by('-create_time')