from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import Repository
from .serializers import RepositorySerializer


class IndexView(APIView):
    def get(self, request):
        return Response("REPOSITORY SERVICE")


class RepositoryDetailView(RetrieveAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class RepositoryCreateView(APIView):
    def post(self, request):
        return Response("CREATE REPOSITORY")
