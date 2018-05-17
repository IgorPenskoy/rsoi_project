from rest_framework.serializers import ModelSerializer

from .models import Repository


class RepositorySerializer(ModelSerializer):
    class Meta:
        model = Repository
        fields = ('id', 'url', 'username', 'repository', 'last_activity',)
