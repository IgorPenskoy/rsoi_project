from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

####################################################################################################


from requests import codes
from requests.exceptions import ConnectionError


####################################################################################################


from .functions import success_response
from .functions import get_auth_header
from .functions import validate_field
from .functions import username_and_password


####################################################################################################


from .functions import login
from .functions import logout

####################################################################################################


from .functions import register_user
from .functions import delete_user
from .functions import restore_user


####################################################################################################


from .functions import register_student
from .functions import get_student_list
from .functions import get_student
from .functions import put_student
from .functions import delete_student


####################################################################################################


from .functions import register_mentor
from .functions import get_mentor_list
from .functions import get_mentor
from .functions import put_mentor
from .functions import delete_mentor

####################################################################################################


from .functions import create_work
from .functions import get_work_list
from .functions import get_work
from .functions import put_work
from .functions import delete_work


####################################################################################################


from .functions import create_direction
from .functions import get_direction_list
from .functions import get_direction
from .functions import put_direction
from .functions import delete_direction


####################################################################################################


from .functions import create_dist_auto
from .functions import get_dist
from .functions import put_dist
from .functions import delete_dist


####################################################################################################


from .functions import get_repo
from .functions import create_repository


####################################################################################################


from .functions import can_change_student
from .functions import can_change_mentor
from .functions import can_add_work
from .functions import can_edit_work
from .functions import can_delete_work
from .functions import can_add_direction
from .functions import can_edit_direction
from .functions import can_delete_direction
from .functions import can_edit_distribution
from .functions import can_delete_distribution
from .functions import can_create_repository


####################################################################################################


from .constants import STUDENT_GROUP
from .constants import MENTOR_GROUP
from .constants import SUCCESS_LOGOUT
from .constants import NAME_RE
from .constants import SUCCESS_REGISTRATION
from .constants import SUCCESS_DELETE
from .constants import WORK_RE


####################################################################################################


from .exceptions import InternalError
from .exceptions import ServiceUnavailable
from .exceptions import catch_exceptions


####################################################################################################


class IndexView(APIView):
    @catch_exceptions
    def get(self, request):
        return success_response()


####################################################################################################


class LoginView(APIView):
    @catch_exceptions
    def post(self, request):
        auth_response = login(
            request.data.get("username"),
            request.data.get("password"),
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


####################################################################################################


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
        science_preferences = validate_field("science_preferences",
                                             request.data.get("science_preferences"))
        personal_preferences = validate_field("personal_preferences",
                                              request.data.get("personal_preferences"))
        auth_header = get_auth_header(request)
        auth_response = can_change_student(pk, auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_student(pk, name, surname, patronymic, group, email,
                                                science_preferences, personal_preferences)
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


####################################################################################################


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
        science_preferences = validate_field("science_preferences",
                                             request.data.get("science_preferences"))
        personal_preferences = validate_field("personal_preferences",
                                              request.data.get("personal_preferences"))
        auth_header = get_auth_header(request)
        auth_response = can_change_mentor(pk, auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_mentor(pk, name, surname, patronymic, email, position, title,
                                               science_preferences, personal_preferences)
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


####################################################################################################


class WorkListView(APIView):
    @catch_exceptions
    def get(self, request):
        distribution_response = get_work_list()
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def post(self, request):
        title = validate_field("title", request.data.get("title"), True, True, WORK_RE)
        course = validate_field("course", request.data.get("course"), True, True)
        semester = validate_field("semester", request.data.get("semester"), True, True)
        directions = validate_field("directions", request.data.get("directions"))

        auth_header = get_auth_header(request)
        auth_response = can_add_work(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = create_work(title, course, semester, directions)
            if distribution_response.status_code == codes.created:
                return success_response(detail=distribution_response.json())
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


class WorkView(APIView):
    @catch_exceptions
    def get(self, request, pk):
        distribution_response = get_work(pk)
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def put(self, request, pk):
        title = validate_field("title", request.data.get("title"), True, True, WORK_RE)
        course = validate_field("course", request.data.get("course"), True, True)
        semester = validate_field("semester", request.data.get("semester"), True, True)
        directions = validate_field("directions", request.data.get("directions"))

        auth_header = get_auth_header(request)
        auth_response = can_edit_work(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_work(pk, title, course, semester, directions)
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

    @catch_exceptions
    def delete(self, request, pk):
        auth_header = get_auth_header(request)
        auth_response = can_delete_work(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = delete_work(pk)
            if distribution_response.status_code == codes.no_content:
                return success_response(status=HTTP_204_NO_CONTENT)
            elif distribution_response.status_code == codes.not_found:
                raise NotFound
            else:
                raise InternalError
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        else:
            raise InternalError


####################################################################################################


class DirectionListView(APIView):
    @catch_exceptions
    def get(self, request):
        distribution_response = get_direction_list()
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        else:
            raise InternalError

    @catch_exceptions
    def post(self, request):
        title = validate_field("title", request.data.get("title"), True, True, WORK_RE)

        auth_header = get_auth_header(request)
        auth_response = can_add_direction(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = create_direction(title)
            if distribution_response.status_code == codes.created:
                return success_response(detail=distribution_response.json())
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


class DirectionView(APIView):
    @catch_exceptions
    def get(self, request, pk):
        distribution_response = get_direction(pk)
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def put(self, request, pk):
        title = validate_field("title", request.data.get("title"), True, True, WORK_RE)

        auth_header = get_auth_header(request)
        auth_response = can_edit_direction(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_direction(pk, title)
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

    @catch_exceptions
    def delete(self, request, pk):
        auth_header = get_auth_header(request)
        auth_response = can_delete_direction(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = delete_direction(pk)
            if distribution_response.status_code == codes.no_content:
                return success_response(status=HTTP_204_NO_CONTENT)
            elif distribution_response.status_code == codes.not_found:
                raise NotFound
            else:
                raise InternalError
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        else:
            raise InternalError


####################################################################################################


class DistributionListView(APIView):
    @catch_exceptions
    def get(self, request, work_id, group):
        distribution_response = get_dist(work_id, group)
        if distribution_response.status_code == codes.ok:
            return success_response(detail=distribution_response.json())
        elif distribution_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def post(self, request, work_id, group):
        auth_header = get_auth_header(request)
        auth_response = can_edit_distribution(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = create_dist_auto(work_id, group)
            if distribution_response.status_code == codes.ok:
                return success_response(message=distribution_response.json())
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


class DistributionView(APIView):
    @catch_exceptions
    def put(self, request, pk):
        work_id = validate_field("work_id", request.data.get("work_id"), True, True)
        mentor_id = validate_field("mentor_id", request.data.get("mentor_id"), True, True)
        student_id = validate_field("student_id", request.data.get("student_id"), True, True)

        auth_header = get_auth_header(request)
        auth_response = can_edit_distribution(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = put_dist(pk, work_id, mentor_id, student_id)
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

    @catch_exceptions
    def delete(self, request, pk):
        auth_header = get_auth_header(request)
        auth_response = can_delete_distribution(auth_header)
        if auth_response.status_code == codes.ok:
            distribution_response = delete_dist(pk)
            if distribution_response.status_code == codes.no_content:
                return success_response(status=HTTP_204_NO_CONTENT)
            elif distribution_response.status_code == codes.not_found:
                raise NotFound
            else:
                raise InternalError
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        else:
            raise InternalError


####################################################################################################


class RepositoryView(APIView):
    @catch_exceptions
    def get(self, request, user_id):
        repository_response = get_repo(user_id)
        print(repository_response.content)
        if repository_response.status_code == codes.ok:
            return success_response(detail=repository_response.json())
        elif repository_response.status_code == codes.not_found:
            raise NotFound
        else:
            raise InternalError

    @catch_exceptions
    def post(self, request, user_id):
        private_key = validate_field("private_key", request.data.get("private_key"), True, True)
        repository_name = validate_field("repository_name", request.data.get("repository_name"), True, True)

        auth_header = get_auth_header(request)
        auth_response = can_create_repository(auth_header)
        if auth_response.status_code == codes.ok:
            repository_response = create_repository(user_id, private_key, repository_name)
            if repository_response.status_code == codes.ok:
                return success_response(message=repository_response.json())
            elif repository_response.status_code == codes.bad_request:
                raise ValidationError(detail=repository_response.json())
            else:
                raise InternalError
        elif auth_response.status_code == codes.unauthorized:
            raise NotAuthenticated
        elif auth_response.status_code == codes.forbidden:
            raise PermissionDenied
        else:
            raise InternalError


####################################################################################################


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
def forbidden_error(request, exception):
    raise PermissionDenied
