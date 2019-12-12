from rest_framework import serializers
from soup.models import Soup


class SoupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soup
        fields = ('id', 'content')