from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import Repository
from .serializers import RepositorySerializer
from .functions import create_repository
from .functions import update_repository_info


class IndexView(APIView):
    def get(self, request):
        return Response("REPOSITORY SERVICE")


class RepositoryDetailView(RetrieveAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def get(self, request, *args, **kwargs):
        update_repository_info(kwargs["pk"])
        return super(RepositoryDetailView, self).get(request, args, kwargs)


class RepositoryCreateView(APIView):
    def post(self, request):
        data = request.data
        private_token = data.get("private_token")
        repository_name = data.get("repository_name")
        create_repository(repository_name, private_token)
        return Response("CREATE REPOSITORY")
