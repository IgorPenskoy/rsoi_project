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
REPOSITORY_URL = settings.REPOSITORY_URL


####################################################################################################


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
    elif check_re and not re.match(check_re.get("re"), str(field_value)):
        raise ValidationError({field_name: check_re.get("message")})
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


####################################################################################################


def get(url, params=None, headers=None):
    return requests.get(url, params=params, headers=headers)


def post(url, request_json=None, headers=None):
    return requests.post(url, json=request_json, headers=headers)


def put(url, request_json=None, headers=None):
    return requests.put(url, json=request_json, headers=headers)


def delete(url, request_json=None, headers=None):
    return requests.delete(url, json=request_json, headers=headers)


####################################################################################################


def get_auth(url, params=None, auth_header=None):
    headers = {"Authorization": auth_header}
    return get(AUTH_URL + url, params, headers=headers)


def post_auth(url, request_json=None, auth_header=None):
    headers = {"Authorization": auth_header}
    return post(AUTH_URL + url, request_json, headers=headers)


def delete_auth(url, request_json=None, auth_header=None):
    headers = {"Authorization": auth_header}
    return delete(AUTH_URL + url, request_json, headers=headers)


####################################################################################################


def get_distribution(url, params=None):
    return get(DISTRIBUTION_URL + url, params)


def post_distribution(url, request_json=None):
    return post(DISTRIBUTION_URL + url, request_json)


def put_distribution(url, request_json=None):
    return put(DISTRIBUTION_URL + url, request_json)


def delete_distribution(url, request_json=None):
    return delete(DISTRIBUTION_URL + url, request_json)


####################################################################################################


def get_repository(url, params=None):
    return get(REPOSITORY_URL + url, params)


def post_repository(url, request_json=None):
    return post(REPOSITORY_URL + url, request_json)


####################################################################################################


def login(username, password):
    request_json = {
        "username": username,
        "password": password,
    }
    return post_auth("rest-auth/login/", request_json)


def logout(auth_header=None):
    return post_auth("rest-auth/logout/", auth_header=auth_header)


####################################################################################################


def register_user(username, password, group, auth_header):
    request_json = {
        "username": username,
        "password1": password,
        "password2": password,
        "group": group,
    }
    return post_auth("rest-auth/registration/", request_json, auth_header=auth_header)


def delete_user(uid, auth_header):
    return delete_auth("delete/%s/" % str(uid), auth_header=auth_header)


def restore_user(uid, auth_header):
    return post_auth("restore/%s/" % str(uid), auth_header=auth_header)


####################################################################################################


def get_student(pk):
    return get_distribution("student/%s/" % str(pk))


def get_student_list(group):
    return get_distribution("student/group/%s/" % str(group))


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


def put_student(pk, name, surname, patronymic, email, group,
                science_preferences, personal_preferences):
    request_json = {
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "email": email,
        "group": group,
        "science_preferences": science_preferences,
        "personal_preferences": personal_preferences,
    }
    return put_distribution("student/%s/" % str(pk), request_json)


def delete_student(uid):
    return delete_distribution("student/%s/" % str(uid))


####################################################################################################


def get_mentor(pk):
    return get_distribution("mentor/%s/" % str(pk))


def get_mentor_list():
    return get_distribution("mentor/")


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


def put_mentor(pk, name, surname, patronymic, email, position, title,
               science_preferences, personal_preferences):
    request_json = {
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "email": email,
        "position": position,
        "title": title,
        "science_preferences": science_preferences,
        "personal_preferences": personal_preferences,
    }
    return put_distribution("mentor/%s/" % str(pk), request_json)


def delete_mentor(uid):
    return delete_distribution("mentor/%s/" % str(uid))


####################################################################################################


def get_work(pk):
    return get_distribution("work/%s/" % str(pk))


def get_work_list():
    return get_distribution("work/")


def create_work(title, course, semester, directions):
    request_json = {
        "title": title,
        "course": course,
        "semester": semester,
        "directions": directions,
    }
    return post_distribution("work/", request_json)


def put_work(pk, title, course, semester, directions):
    request_json = {
        "title": title,
        "course": course,
        "semester": semester,
        "directions": directions,
    }
    return put_distribution("work/%s/" % str(pk), request_json)


def delete_work(uid):
    return delete_distribution("work/%s/" % str(uid))


####################################################################################################


def get_direction(pk):
    return get_distribution("direction/%s/" % str(pk))


def get_direction_list():
    return get_distribution("direction/")


def create_direction(title):
    request_json = {
        "title": title,
    }
    return post_distribution("direction/", request_json)


def put_direction(pk, title):
    request_json = {
        "title": title,
    }
    return put_distribution("direction/%s/" % str(pk), request_json)


def delete_direction(pk):
    return delete_distribution("direction/%s/" % str(pk))


####################################################################################################


def get_dist(work_id, group):
    return get_distribution("distribution/work/%s/group/%s/" % (str(work_id), str(group)))


def create_dist_auto(work_id, group):
    return post_distribution("distribution/auto/work/%s/group/%s/" % (str(work_id), str(group)))


def create_dist(work_id, student_id, mentor_id):
    request_json = {
        "work_id": work_id,
        "student_id": student_id,
        "mentor_id": mentor_id,
    }
    return post_distribution("distribution/", request_json)


def put_dist(pk, work_id, student_id, mentor_id):
    request_json = {
        "work_id": work_id,
        "student_id": student_id,
        "mentor_id": mentor_id,
    }
    return put_distribution("distribution/%s/" % str(pk), request_json)


def delete_dist(pk):
    return delete_distribution("distribution/%s/" % str(pk))


####################################################################################################


def get_repo(user_id):
    return get_repository("repository/%s/" % str(user_id))


def create_repository(user_id, private_key, name):
    request_json = {
        "user_id": user_id,
        "private_key": private_key,
        "repository_name": name,
    }
    return post_repository("repository/create/", request_json=request_json)


####################################################################################################


def can_change_student(pk, auth_header):
    return get_auth("check/can_edit_student_info/%s/" % str(pk), auth_header=auth_header)


def can_change_mentor(pk, auth_header):
    return get_auth("check/can_edit_mentor_info/%s/" % str(pk), auth_header=auth_header)


def can_add_work(auth_header):
    return get_auth("check/can_add_work/", auth_header=auth_header)


def can_edit_work(auth_header):
    return get_auth("check/can_edit_work/", auth_header=auth_header)


def can_delete_work(auth_header):
    return get_auth("check/can_delete_work/", auth_header=auth_header)


def can_add_direction(auth_header):
    return get_auth("check/can_add_direction/", auth_header=auth_header)


def can_edit_direction(auth_header):
    return get_auth("check/can_edit_direction/", auth_header=auth_header)


def can_delete_direction(auth_header):
    return get_auth("check/can_delete_direction/", auth_header=auth_header)


def can_edit_distribution(auth_header):
    return get_auth("check/can_edit_distribution/", auth_header=auth_header)


def can_delete_distribution(auth_header):
    return get_auth("check/can_delete_distribution/", auth_header=auth_header)


def can_create_repository(auth_header):
    return get_auth("check/can_add_repository/", auth_header=auth_header)
