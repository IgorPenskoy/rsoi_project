from django.views import View
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from requests import codes

from .functions import login
from .functions import logout
from .functions import get_auth_token
from .functions import set_context

from .functions import check_cookies
from .functions import set_cookies
from .functions import delete_cookies
from .functions import catch_exceptions
from .functions import page_error
from .functions import template_path


from .constants import INTERNAL_ERROR
from .constants import NOT_FOUND
from .constants import FORBIDDEN
from .constants import BAD_REQUEST


class IndexView(View):
    @catch_exceptions
    def get(self, request):
        return render(request, template_path("index"))


class LoginView(View):
    @catch_exceptions
    def get(self, request, *args, **kwargs):
        return render(request, template_path("login"))

    @catch_exceptions
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        response = login(username, password)
        response_json = response.json()
        error = response_json.get("error")
        context = set_context(error)

        if error:
            context["username_restore"] = username
            return render(request, template_path("login"),
                          status=response.status_code,
                          context=context)

        out = redirect("index")
        detail = response_json.get("detail")
        auth_token = detail.get("token")
        group = None
        user_id = None
        user = detail.get("user")
        if user:
            user_id = user.get("pk")
            groups = user.get("groups")
            if groups:
                group = groups[0].get("name")
                if not group:
                    group = "admin"
            else:
                group = "admin"

        out = set_cookies(out, auth_token, username, user_id, group)

        print(out.cookies)

        return out


class LogoutView(View):
    @catch_exceptions
    def get(self, request, *args, **kwargs):
        auth_token = get_auth_token(request)
        logout(auth_token)
        out = redirect("index")
        delete_cookies(out)

        return out


def internal_error(request):
    return page_error(request, 500, INTERNAL_ERROR)


def not_found_error(request, exception):
    return page_error(request, 404, NOT_FOUND)


def bad_request_error(request, exception):
    return page_error(request, 400, BAD_REQUEST)


def forbidden_error(request, exception):
    return page_error(request, 403, FORBIDDEN)
