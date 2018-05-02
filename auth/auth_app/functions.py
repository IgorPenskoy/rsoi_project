from rest_framework.response import Response

from auth_app.constants import APP_LABEL


def check_permission_answer(user, permission_name):
    if user.has_perm("%s.%s" % (APP_LABEL, permission_name)):
        return Response({"access": True})
    return Response({"access": False})
