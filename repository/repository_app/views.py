from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_404_NOT_FOUND
from datetime import datetime
from .models import Repository
from .functions import create_repository
from .functions import update_repository_info


class IndexView(APIView):
    def get(self, request):
        return Response("REPOSITORY SERVICE")


class RepositoryDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            repository = Repository.objects.get(user_id=int(kwargs.get("pk")))
            update_repository_info(repository.pk)
            repository = Repository.objects.get(user_id=int(kwargs.get("pk")))

            return Response(data={
                    "url": repository.url,
                    "name": repository.repository,
                    "username": repository.username,
                    "last_activity": str(datetime.astimezone(repository.last_activity).strftime("%d-%m-%Y %H:%M")),
            })
        except Repository.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class RepositoryCreateView(APIView):
    def post(self, request):
        try:
            data = request.data
            private_token = data.get("private_key")
            repository_name = data.get("repository_name")
            user_id = data.get("user_id")
            create_repository(repository_name, private_token, user_id)
        except Exception:
            Response(status=HTTP_400_BAD_REQUEST, data={u"Некорректные входные данные"})
        return Response(u"Успешно создан репозиторий")
