import re
import requests

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .exceptions import ValidationError
from .constants import MANDATORY_FIELD
from .constants import NOT_EMPTY_FIELD

from .transliterate import transliterate

AUTH_URL = settings.AUTH_URL
DISTRIBUTION_URL = settings.DISTRIBUTION_URL


def username_and_password(surname, name, patronymic, username=None, password=None):
    if not username:
        username = transliterate(surname.lower()) + \
                   transliterate(name[0].lower()) + \
                   transliterate(patronymic[0].lower())
    if not password:
        password = User.objects.make_random_password()

    return username, password


def validate_field(field_name, field_value, mandatory=False, not_empty=False, check_re=None):
    if mandatory and field_value is None:
        raise ValidationError({field_name: MANDATORY_FIELD})
    elif not_empty and not str(field_value).strip():
        raise ValidationError({field_name: NOT_EMPTY_FIELD})
    elif check_re and not re.match(check_re, str(field_value)):
        raise ValidationError({field_name: check_re})
    return field_value


def response_convert(requests_response):
    data = requests_response.json()
    status_code = requests_response.status_code
    data["status_code"] = status_code
    response = Response(
        data=data,
        status=status_code,
        content_type=requests_response.headers.get('Content-Type')
    )
    return response


def get_auth_header(request):
    return request.META.get("HTTP_AUTHORIZATION")


def success_response(message=None, status=HTTP_200_OK, detail=None):
    return Response({"message": message, "status_code": status, "detail": detail}, status=status)


def post(url, request_json=None, headers=None):
    return requests.post(url, json=request_json, headers=headers)


def delete(url, request_json=None, headers=None):
    return requests.delete(url, json=request_json, headers=headers)


def post_auth(url, request_json=None, auth_header=None):
    headers = {"Authorization": auth_header}
    return post(AUTH_URL + url, request_json, headers=headers)


def delete_auth(url, request_json=None, auth_header=None):
    headers = {"Authorization": auth_header}
    return delete(AUTH_URL + url, request_json, headers=headers)


def post_distribution(url, request_json):
    return post(DISTRIBUTION_URL + url, request_json)


def delete_distribution(url, request_json=None, auth_header=None):
    headers = {"Authorization": auth_header}
    return delete(DISTRIBUTION_URL + url, request_json, headers=headers)


def login(username, password):
    request_json = {
        "username": username,
        "password": password,
    }
    return post_auth("rest-auth/login/", request_json)


def logout(auth_header=None):
    return post_auth("rest-auth/logout/", auth_header=auth_header)


def register_user(username, password, group, auth_header):
    request_json = {
        "username": username,
        "password1": password,
        "password2": password,
        "group": group,
    }
    return post_auth("rest-auth/registration/", request_json, auth_header=auth_header)


def register_student(uid, name, surname, patronymic, email, group):
    request_json = {
        "id": uid,
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "email": email,
        "group": group,
    }
    return post_distribution("student/", request_json)


def register_mentor(uid, name, surname, patronymic, email, position, title):
    request_json = {
        "id": uid,
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "email": email,
        "position": position,
        "title": title,
    }
    return post_distribution("mentor/", request_json)


def delete_user(uid, auth_header):
    return delete_auth("delete/%s/" % str(uid), auth_header=auth_header)


def restore_user(uid, auth_header):
    return post_auth("restore/%s/" % str(uid), auth_header=auth_header)


def delete_student(uid):
    return delete_distribution("student/%s/" % str(uid))


def delete_mentor(uid):
    return delete_distribution("mentor/%s/" % str(uid))
