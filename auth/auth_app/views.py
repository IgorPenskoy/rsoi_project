from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_auth.views import LogoutView

from .functions import check_permission_answer


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


class CanAddMentor(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_add_mentor")


class CanAddStudent(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_add_student")


class CanEditStudentInfo(APIView):
    def get(self, request, pk):
        if request.user.pk == int(pk):
            return Response()
        else:
            return check_permission_answer(request.user, "can_edit_student_info")


class CanEditMentorInfo(APIView):
    def get(self, request, pk):
        if request.user.pk == int(pk):
            return Response()
        else:
            return check_permission_answer(request.user, "can_edit_mentor_info")


class CanDeleteUser(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_delete_user")


class CanEditDistribution(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_edit_distribution")


class CanMakeDistribution(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_make_distribution")


class CanAddWork(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_add_work")


class CanDeleteWork(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_delete_work")


class CanDeleteDirection(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_delete_direction")


class CanAddRepository(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_add_repository")


class CanAddDirection(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_add_direction")


class CanEditWork(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_edit_work")


class CanWatchStudentList(APIView):
    def get(self, request):
        return check_permission_answer(request.user, "can_watch_student_list")


class CanWatchStudentInfo(APIView):
    def get(self, request, pk):
        if request.user.pk == int(pk):
            return Response()
        else:
            return check_permission_answer(request.user, "can_watch_student_info")
