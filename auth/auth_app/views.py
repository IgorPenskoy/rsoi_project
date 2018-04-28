from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_auth.views import LogoutView


class IndexView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return Response()


class AuthView(APIView):
    def get(self, request):
        return Response()


class AuthLogoutView(LogoutView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class DeleteUserView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save()
            return Response(status=HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            raise NotFound


class RestoreUserView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
            return Response()
        except User.DoesNotExist:
            raise NotFound
