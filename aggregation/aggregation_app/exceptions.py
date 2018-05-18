from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from requests.exceptions import ConnectionError

from .constants import NOT_FOUND_ERROR
from .constants import JSON_ERROR
from .constants import LOGIN_ERROR
from .constants import AUTH_ERROR
from .constants import PERMISSION_DENIED_ERROR
from .constants import NOT_ALLOWED_ERROR
from .constants import NOT_ACCEPTABLE_ERROR
from .constants import UNSUPPORTED_MEDIA_ERROR
from .constants import THROTTLED_ERROR
from .constants import VALIDATION_ERROR


def error_response(error, status_code, detail=None):
    return Response({"error": error, "status_code": status_code, "detail": detail}, status=status_code)


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        return error_response(NOT_FOUND_ERROR, status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, PermissionDenied):
        return error_response(PERMISSION_DENIED_ERROR, status.HTTP_403_FORBIDDEN)
    elif isinstance(exc, exceptions.ParseError):
        return error_response(JSON_ERROR, status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, exceptions.AuthenticationFailed):
        return error_response(LOGIN_ERROR, status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, exceptions.NotAuthenticated):
        return error_response(AUTH_ERROR, status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, exceptions.PermissionDenied):
        return error_response(PERMISSION_DENIED_ERROR, status.HTTP_403_FORBIDDEN)
    elif isinstance(exc, exceptions.NotFound):
        return error_response(NOT_FOUND_ERROR, status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, exceptions.MethodNotAllowed):
        return error_response(NOT_ALLOWED_ERROR, status.HTTP_405_METHOD_NOT_ALLOWED)
    elif isinstance(exc, exceptions.NotAcceptable):
        return error_response(NOT_ACCEPTABLE_ERROR, status.HTTP_406_NOT_ACCEPTABLE)
    elif isinstance(exc, exceptions.UnsupportedMediaType):
        return error_response(UNSUPPORTED_MEDIA_ERROR, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    elif isinstance(exc, exceptions.Throttled):
        return error_response(THROTTLED_ERROR, status.HTTP_429_TOO_MANY_REQUESTS)
    elif isinstance(exc, exceptions.ValidationError):
        return error_response(VALIDATION_ERROR, status.HTTP_400_BAD_REQUEST, exc.detail)

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error'] = exc.detail
    return response


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = u'Сервис временно недоступен, попробуйте повторить действие позже'
    default_code = 'service_unavailable'


class InternalError(APIException):
    status_code = 500
    default_detail = u'Внутренняя ошибка сервера, попробуйте повторить действие позже'
    default_code = 'internal_error'


class ValidationError(exceptions.ValidationError):
    status_code = 400
    default_detail = u"Некорректные входные данные"
    default_code = "validation_error"


def catch_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (APIException, Http404, PermissionDenied, InternalError) as e:
            raise e
        except ConnectionError:
            raise ServiceUnavailable
        except Exception:
            raise InternalError
    return wrapper
