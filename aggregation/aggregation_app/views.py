from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from requests import codes
from requests.exceptions import ConnectionError

from .functions import login
from .functions import logout
from .functions import delete_student
from .functions import delete_mentor
from .functions import delete_user
from .functions import restore_user
from .functions import register_user
from .functions import register_student
from .functions import register_mentor
from .functions import success_response
from .functions import get_auth_header
from .functions import validate_field
from .functions import username_and_password
from .functions import get_student_list
from .functions import can_change_student
from .functions import can_change_mentor
from .functions import get_student
from .functions import put_student
from .functions import get_mentor
from .functions import put_mentor
from .functions import get_mentor_list

from .constants import STUDENT_GROUP
from .constants import MENTOR_GROUP
from .constants import SUCCESS_LOGOUT
from .constants import NAME_RE
from .constants import SUCCESS_REGISTRATION
from .constants import SUCCESS_DELETE

from .exceptions import InternalError
from .exceptions import ServiceUnavailable
from .exceptions import catch_exceptions


class IndexView(APIView):
    @catch_exceptions
    def get(self, request):
        return success_response()


class LoginView(APIView):
    @catch_exceptions
    def post(self, request):
        auth_response = login(
            validate_field("username", request.data.get("username"), True, True),
            validate_field("password", request.data.get("password"), True, True)
        )
        if auth_response.status_code == codes.ok:
            return success_response(detail=auth_response.json())
        elif auth_response.status_code == codes.bad_request:
            raise AuthenticationFailed
        else:
            raise InternalError


class LogoutView(APIView):
    @catch_exceptions
    def post(self, request):
        auth_header = get_auth_header(request)
        auth_response = logout(auth_header)
        if auth_response.status_code == codes.ok:
            return success_response(SUCCESS_LOGOUT)
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        else:
            raise InternalError


class ListStudentView(APIView):
    @catch_exceptions
    def get(self, request, group):
        distribution_response = get_student_list(group)
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError


class StudentView(APIView):
    @catch_exceptions
    def get(self, request, pk):
        distribution_response = get_student(pk)
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def put(self, request, pk):
        name = validate_field("name", request.data.get("name"), True, True, NAME_RE)
        surname = validate_field("surname", request.data.get("surname"), True, True, NAME_RE)
        patronymic = validate_field("patronymic", request.data.get("patronymic"), True, True, NAME_RE)
        group = validate_field("group", request.data.get("group"), True, True)
        email = validate_field("email", request.data.get("email"))
        auth_header = get_auth_header(request)
        auth_response = can_change_student(pk, auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_student(pk, name, surname, patronymic, group, email)
            if distribution_response.status_code == codes.ok:
                return success_response(detail=distribution_response.json())
            elif distribution_response.status_code == codes.not_found:
                raise NotFound
            elif distribution_response.status_code == codes.bad_request:
                raise ValidationError(detail=distribution_response.json())
            else:
                raise InternalError
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        else:
            raise InternalError


class RegistrationStudentView(APIView):
    @catch_exceptions
    def post(self, request):
        name = validate_field("name", request.data.get("name"), True, True, NAME_RE)
        surname = validate_field("surname", request.data.get("surname"), True, True, NAME_RE)
        patronymic = validate_field("patronymic", request.data.get("patronymic"), True, True, NAME_RE)
        group = validate_field("group", request.data.get("group"), True, True)
        email = validate_field("email", request.data.get("email"))
        username, password = username_and_password(
            surname, name, patronymic,
            validate_field("username", request.data.get("username")),
            validate_field("password", request.data.get("password")),
        )
        auth_header = get_auth_header(request)
        auth_response = register_user(username, password, STUDENT_GROUP, auth_header)
        if auth_response.status_code == codes.created:
            uid = auth_response.json()["user"]["pk"]
            try:
                distribution_response = register_student(uid, name, surname, patronymic, email, group)
                if distribution_response.status_code == codes.created:
                    data = distribution_response.json()
                    data["username"] = username
                    data["password"] = password
                    return success_response(SUCCESS_REGISTRATION, detail=data)
                elif distribution_response.status_code == codes.bad_request:
                    delete_user(uid, auth_header)
                    raise ValidationError(detail=distribution_response.json())
                else:
                    delete_user(uid, auth_header)
                    raise InternalError
            except ConnectionError:
                delete_user(uid, auth_header)
                raise ServiceUnavailable
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        elif auth_response.status_code == codes.bad_request:
            raise ValidationError(detail=auth_response.json())
        else:
            raise InternalError


class DeleteStudentView(APIView):
    @catch_exceptions
    def delete(self, request, pk):
        auth_header = get_auth_header(request)
        auth_response = delete_user(pk, auth_header)
        if auth_response.status_code == codes.no_content:
            try:
                distribution_response = delete_student(pk)
                if distribution_response.status_code == codes.no_content:
                    return success_response(SUCCESS_DELETE, HTTP_204_NO_CONTENT)
                elif distribution_response.status_code == codes.not_found:
                    restore_user(pk, auth_header)
                    raise NotFound
                else:
                    restore_user(pk, auth_header)
                    raise InternalError
            except ConnectionError:
                restore_user(pk, auth_header)
                raise ServiceUnavailable
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        elif auth_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError


class ListMentorView(APIView):
    @catch_exceptions
    def get(self, request):
        distribution_response = get_mentor_list()
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError


class MentorView(APIView):
    @catch_exceptions
    def get(self, request, pk):
        distribution_response = get_mentor(pk)
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def put(self, request, pk):
        name = validate_field("name", request.data.get("name"), True, True, NAME_RE)
        surname = validate_field("surname", request.data.get("surname"), True, True, NAME_RE)
        patronymic = validate_field("patronymic", request.data.get("patronymic"), True, True, NAME_RE)
        position = validate_field("position", request.data.get("position"), True, True)
        title = validate_field("title", request.data.get("title"))
        email = validate_field("email", request.data.get("email"))
        auth_header = get_auth_header(request)
        auth_response = can_change_mentor(pk, auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_mentor(pk, name, surname, patronymic, email, position, title)
            if distribution_response.status_code == codes.ok:
                return success_response(detail=distribution_response.json())
            elif distribution_response.status_code == codes.not_found:
                raise NotFound
            elif distribution_response.status_code == codes.bad_request:
                raise ValidationError(detail=distribution_response.json())
            else:
                raise InternalError
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        else:
            raise InternalError


class RegistrationMentorView(APIView):
    @catch_exceptions
    def post(self, request):
        name = validate_field("name", request.data.get("name"), True, True, NAME_RE)
        surname = validate_field("surname", request.data.get("surname"), True, True, NAME_RE)
        patronymic = validate_field("patronymic", request.data.get("patronymic"), True, True, NAME_RE)
        position = validate_field("position", request.data.get("position"), True, True)
        title = validate_field("title", request.data.get("title"))
        email = validate_field("email", request.data.get("email"))
        username, password = username_and_password(
            surname, name, patronymic,
            validate_field("username", request.data.get("username")),
            validate_field("password", request.data.get("password")),
        )
        auth_header = get_auth_header(request)
        auth_response = register_user(username, password, MENTOR_GROUP, auth_header)
        if auth_response.status_code == codes.created:
            uid = auth_response.json()["user"]["pk"]
            try:
                distribution_response = register_mentor(uid, name, surname, patronymic,
                                                        email, position, title)
                if distribution_response.status_code == codes.created:
                    data = distribution_response.json()
                    data["username"] = username
                    data["password"] = password
                    return success_response(SUCCESS_REGISTRATION, detail=data)
                elif distribution_response.status_code == codes.bad_request:
                    delete_user(uid, auth_header)
                    raise ValidationError(detail=distribution_response.json())
                else:
                    delete_user(uid, auth_header)
                    raise InternalError
            except ConnectionError:
                delete_user(uid, auth_header)
                raise ServiceUnavailable
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        elif auth_response.status_code == codes.bad_request:
            raise ValidationError(detail=auth_response.json())
        else:
            raise InternalError


class DeleteMentorView(APIView):
    @catch_exceptions
    def delete(self, request, pk):
        auth_header = get_auth_header(request)
        auth_response = delete_user(pk, auth_header)
        if auth_response.status_code == codes.no_content:
            try:
                distribution_response = delete_mentor(pk)
                if distribution_response.status_code == codes.no_content:
                    return success_response(SUCCESS_DELETE, HTTP_204_NO_CONTENT)
                elif distribution_response.status_code == codes.not_found:
                    restore_user(pk, auth_header)
                    raise NotFound
                else:
                    restore_user(pk, auth_header)
                    raise InternalError
            except ConnectionError:
                restore_user(pk, auth_header)
                raise ServiceUnavailable
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        elif auth_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError


@api_view(["GET", "POST"])
def internal_error(request):
    raise InternalError


@api_view(["GET", "POST"])
def not_found_error(request, exception):
    raise NotFound


@api_view(["GET", "POST"])
def bad_request_error(request, exception):
    raise ValidationError


@api_view(["GET", "POST"])
def not_found_error(request, exception):
    raise PermissionDenied
