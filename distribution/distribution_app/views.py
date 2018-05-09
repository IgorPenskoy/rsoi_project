from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class IndexView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return Response("DISTRIBUTION SERVICE")
