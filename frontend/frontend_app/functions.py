import requests

from requests.exceptions import ConnectionError
from django.conf import settings
from django.shortcuts import render

from .constants import SERVICE_UNAVAILABLE
from .constants import INTERNAL_ERROR

AGGREGATION_URL = settings.AGGREGATION_URL


def template_path(name):
    return "frontend_app/" + str(name) + ".html"


def get_auth_token(request):
    return request.COOKIES.get("auth_token")


def post(url, request_json=None, auth_token=None):
    headers=None
    if auth_token:
        headers = {"Authorization": "JWT " + str(auth_token)}
    return requests.post(AGGREGATION_URL + url, json=request_json, headers=headers)


def login(username, password):
    reqest_json = {
        "username": username,
        "password": password,
    }
    return post("login/", request_json=reqest_json)


def logout(auth_token):
    return post("logout/", auth_token=auth_token)


def set_context(error=None):
    context = {
        "error": error,
    }
    return context


def check_cookies(request):
    cookies = request.COOKIES
    auth_token = cookies.get("auth_token")
    username = cookies.get("username")
    user_id = cookies.get("user_id")
    group = cookies.get("group")

    if all([auth_token, username, user_id, group]):
        return True

    return False


def set_cookies(response, auth_token, username, user_id, group):
    response.set_cookie("auth_token", auth_token)
    response.set_cookie("username", username)
    response.set_cookie("user_id", user_id)
    response.set_cookie("group", group)

    return response


def delete_cookies(response):
    response.delete_cookie("auth_token")
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    response.delete_cookie("group")

    return response


def page_error(request, status, message):
    return render(request,
                  template_path("error"),
                  context={
                      "status_code": status,
                      "error_description": message})


def catch_exceptions(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except ConnectionError:
            return page_error(request, 503, SERVICE_UNAVAILABLE)
        except Exception:
            return page_error(request, 500, INTERNAL_ERROR)
    return wrapper
