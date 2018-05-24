from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect

from requests import codes


#########################################################################################


from .functions import login
from .functions import logout
from .functions import get_auth_token
from .functions import handle_response


#########################################################################################


from .functions import set_cookies
from .functions import delete_cookies
from .functions import catch_exceptions
from .functions import page_error
from .functions import template_path


#########################################################################################


from .functions import get_work_list
from .functions import get_work
from .functions import put_work
from .functions import post_work
from .functions import delete_work
from .functions import context_work


#########################################################################################


from .functions import get_direction_list
from .functions import get_direction
from .functions import put_direction
from .functions import post_direction
from .functions import delete_direction
from .functions import context_direction


#########################################################################################


from .functions import get_mentor_list
from .functions import get_mentor
from .functions import put_mentor
from .functions import post_mentor
from .functions import delete_mentor
from .functions import context_mentor


#########################################################################################


from .constants import INTERNAL_ERROR
from .constants import NOT_FOUND
from .constants import FORBIDDEN
from .constants import BAD_REQUEST
from .constants import ADMIN_GROUP_NAME


#########################################################################################


class IndexView(View):
    @catch_exceptions()
    def get(self, request):
        return render(request, template_path("index"))


#########################################################################################


class LoginView(View):
    @catch_exceptions(False)
    def get(self, request, *args, **kwargs):
        return render(request, template_path("login"))

    @catch_exceptions(False)
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        status_code, detail, error = handle_response(login(username, password))

        if error:
            context = {
                "username_restore": username,
                "error": error,
            }
            return render(request, template_path("login"),
                          status=status_code,
                          context=context)

        out = redirect("index")
        auth_token = detail.get("token")
        user = detail.get("user")
        group = None
        user_id = None
        if user:
            user_id = user.get("pk")
            groups = user.get("groups")
            if groups:
                group = groups[0].get("name")
                if not group:
                    group = ADMIN_GROUP_NAME
            else:
                group = ADMIN_GROUP_NAME

        out = set_cookies(out, auth_token, username, user_id, group)

        return out


class LogoutView(View):
    @catch_exceptions(False)
    def get(self, request, *args, **kwargs):
        auth_token = get_auth_token(request)
        logout(auth_token)
        out = redirect("index")
        delete_cookies(out)

        return out


#########################################################################################


class WorkListView(View):
    @catch_exceptions()
    def get(self, request, *args, **kwargs):
        status_code, detail, error = handle_response(get_work_list())
        if error:
            return page_error(request, status_code, error)

        context = {
            "works": detail or [],
        }

        return render(request, template_path("work_list"),
                      context=context, status=status_code)


class WorkDetailView(View):
    @catch_exceptions()
    def get(self, request, pk, *args, **kwargs):
        status_code, work, error = handle_response(get_work(pk))
        if error:
            return page_error(request, status_code, error)
        directions = work.get("directions_detail", [])
        context = context_work(
            work.get("title"),
            work.get("course"),
            work.get("semester"),
            directions,
            w_id=pk,
        )
        return render(request, template_path("work_detail"),
                      context=context, status=status_code)

    @catch_exceptions()
    def post(self, request, pk, *args, **kwargs):
        title = request.POST.get("title")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        directions = request.POST.getlist("directions")

        delete = request.POST.get("delete_input")

        auth_token = get_auth_token(request)
        if delete:
            status_code, detail, error = handle_response(
                delete_work(pk, auth_token)
            )
        else:
            status_code, detail, error = handle_response(
                put_work(pk, title, course, semester, directions, auth_token)
            )

        if status_code == codes.ok or status_code == codes.no_content:
            return redirect("work_list")
        elif status_code == codes.unauthorized:
            return redirect("login")
        elif status_code == codes.bad_request:
            context = context_work(title, course, semester, directions, detail, pk)
            return render(request, template_path("work_detail"),
                          context=context, status=status_code)
        else:
            return page_error(request, status_code, error)


class WorkNewView(View):
    @catch_exceptions()
    def get(self, request, *args, **kwargs):
        if request.COOKIES.get("group") != ADMIN_GROUP_NAME:
            return page_error(request, 404, NOT_FOUND)
        context = context_work()
        return render(request, template_path("work_detail"), context=context)

    @catch_exceptions()
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        directions = request.POST.getlist("directions")
        auth_token = get_auth_token(request)

        status_code, detail, error = handle_response(
            post_work(title, course, semester, directions, auth_token)
        )

        if status_code == codes.ok:
            return redirect("work_list")
        elif status_code == codes.unauthorized:
            return redirect("login")
        elif status_code == codes.bad_request:
            context = context_work(title, course, semester, directions, detail)
            return render(request, template_path("work_detail"),
                          context=context, status=status_code)
        else:
            return page_error(request, status_code, error)


#########################################################################################


class DirectionListView(View):
    @catch_exceptions()
    def get(self, request, *args, **kwargs):
        status_code, detail, error = handle_response(get_direction_list())

        if error:
            return page_error(request, status_code, error)

        context = {
            "directions": detail or [],
        }

        return render(request, template_path("direction_list"),
                      context=context, status=status_code)


class DirectionDetailView(View):
    @catch_exceptions()
    def get(self, request, pk, *args, **kwargs):
        status_code, direction, error = handle_response(get_direction(pk))
        if error:
            return page_error(request, status_code, error)
        context = context_direction(
            title=direction.get("title"),
            d_id=direction.get("id"),
        )
        return render(request, template_path("direction_detail"),
                      context=context, status=status_code)

    @catch_exceptions()
    def post(self, request, pk, *args, **kwargs):
        title = request.POST.get("title")
        delete = request.POST.get("delete_input")
        auth_token = get_auth_token(request)

        if delete:
            status_code, detail, error = handle_response(
                delete_direction(pk, auth_token)
            )
        else:
            status_code, detail, error = handle_response(
                put_direction(pk, title, auth_token)
            )

        if status_code == codes.ok or status_code == codes.no_content:
            return redirect("direction_list")
        elif status_code == codes.unauthorized:
            return redirect("login")
        elif status_code == codes.bad_request:
            context = context_direction(title, detail, pk)
            return render(request, template_path("direction_detail"),
                          context=context, status=status_code)
        else:
            return page_error(request, status_code, error)


class DirectionNewView(View):
    @catch_exceptions()
    def get(self, request, *args, **kwargs):
        if request.COOKIES.get("group") != ADMIN_GROUP_NAME:
            return page_error(request, 404, NOT_FOUND)
        context = context_direction()
        return render(request, template_path("direction_detail"), context=context)

    @catch_exceptions()
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")

        auth_token = get_auth_token(request)

        status_code, detail, error = handle_response(
            post_direction(title, auth_token)
        )

        if status_code == codes.ok:
            return redirect("direction_list")
        elif status_code == codes.unauthorized:
            return redirect("login")
        elif status_code == codes.bad_request:
            context = context_direction(title, detail)
            return render(request, template_path("direction_detail"),
                          context=context, status=status_code)
        else:
            return page_error(request, status_code, error)


#########################################################################################


class MentorListView(View):
    @catch_exceptions()
    def get(self, request, *args, **kwargs):
        status_code, detail, error = handle_response(get_mentor_list())
        if error:
            return page_error(request, status_code, error)

        context = {
            "mentors": detail or [],
        }

        return render(request, template_path("mentor_list"),
                      context=context, status=status_code)


class MentorDetailView(View):
    @catch_exceptions()
    def get(self, request, pk, *args, **kwargs):
        status_code, mentor, error = handle_response(get_mentor(pk))
        if error:
            return page_error(request, status_code, error)
        sciences = mentor.get("science_preferences_detail", [])
        personals = mentor.get("personal_preferences_detail", [])
        context = context_mentor(
            mentor.get("surname"),
            mentor.get("name"),
            mentor.get("patronymic"),
            mentor.get("position"),
            mentor.get("title"),
            mentor.get("email"),
            sciences,
            personals,
            m_id=pk,
        )
        return render(request, template_path("mentor_detail"),
                      context=context, status=status_code)

    @catch_exceptions()
    def post(self, request, pk, *args, **kwargs):
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        position = request.POST.get("position")
        title = request.POST.get("title")
        email = request.POST.get("email")
        sciences = request.POST.getlist("sciences")
        personals = request.POST.getlist("personals")

        delete = request.POST.get("delete_input")

        auth_token = get_auth_token(request)

        if delete:
            status_code, detail, error = handle_response(
                delete_mentor(pk, auth_token)
            )
        else:
            status_code, detail, error = handle_response(
                put_mentor(pk, surname, name, patronymic, position, title, email,
                           sciences, personals, auth_token)
            )

        if status_code == codes.ok or status_code == codes.no_content:
            return redirect("mentor_list")
        elif status_code == codes.unauthorized:
            return redirect("login")
        elif status_code == codes.bad_request:
            context = context_mentor(surname, name, patronymic, position, title,
                                     email, sciences, personals, detail, pk)
            return render(request, template_path("mentor_detail"),
                          context=context, status=status_code)
        else:
            return page_error(request, status_code, error)


class MentorNewView(View):
    @catch_exceptions()
    def get(self, request, *args, **kwargs):
        if request.COOKIES.get("group") != ADMIN_GROUP_NAME:
            return page_error(request, 404, NOT_FOUND)
        context = context_mentor()
        return render(request, template_path("mentor_detail"), context=context)

    @catch_exceptions()
    def post(self, request, *args, **kwargs):
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        position = request.POST.get("position")
        title = request.POST.get("title")
        email = request.POST.get("email")

        auth_token = get_auth_token(request)

        status_code, detail, error = handle_response(
            post_mentor(surname, name, patronymic, position, title, email, auth_token)
        )

        if status_code == codes.ok:
            context = {
                "group": u"Руководитель",
                "username": detail.get("username"),
                "password": detail.get("password"),
            }
            return render(request, template_path("success_registration"), context=context)
        elif status_code == codes.unauthorized:
            return redirect("login")
        elif status_code == codes.bad_request:
            context = context_mentor(surname, name, patronymic, position, title,
                                     email, error_detail=detail)
            return render(request, template_path("mentor_detail"),
                          context=context, status=status_code)
        else:
            return page_error(request, status_code, error)


#########################################################################################


def internal_error(request):
    return page_error(request, 500, INTERNAL_ERROR)


def not_found_error(request, exception):
    return page_error(request, 404, NOT_FOUND)


def bad_request_error(request, exception):
    return page_error(request, 400, BAD_REQUEST)


def forbidden_error(request, exception):
    return page_error(request, 403, FORBIDDEN)
