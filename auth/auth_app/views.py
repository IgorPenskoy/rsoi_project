from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

def index(request):
    return Response("AUTH SERVICE")


class AuthView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response("SUCCESS AUTH USER %s" % request.user.username)
