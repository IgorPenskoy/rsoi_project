from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from auth_app.functions import check_permission_answer


def index(request):
    return Response("AUTH SERVICE")


class AuthView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response("SUCCESS AUTH USER %s" % request.user.username)


class CanAddMentor(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_add_mentor")


class CanAddStudent(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_add_student")


class CanEditStudentInfo(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_edit_student_info")


class CanEditMentorInfo(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_edit_mentor_info")


class CanDeleteUser(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_delete_user")


class CanEditDistribution(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_edit_distribution")


class CanMakeDistribution(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_make_distribution")


class CanAddWork(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_add_work")


class CanDeleteWork(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_delete_work")


class CanDeleteDirection(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_delete_direction")


class CanAddRepository(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_add_repository")


class CanAddDirection(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_add_direction")


class CanEditWork(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_edit_work")


class CanWatchStudentList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_watch_student_list")


class CanWatchStudentInfo(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return check_permission_answer(request.user, "can_watch_student_info")
