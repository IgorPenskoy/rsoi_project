from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from .constants import APP_LABEL


def check_permission_answer(user, permission_name):
    if user.has_perm("%s.%s" % (APP_LABEL, permission_name)):
        return Response()
    return Response(status=HTTP_403_FORBIDDEN)
