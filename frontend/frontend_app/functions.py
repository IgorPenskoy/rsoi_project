import requests

from requests.exceptions import ConnectionError
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect

from .constants import SERVICE_UNAVAILABLE
from .constants import INTERNAL_ERROR
from .constants import COURSES
from .constants import SEMESTERS

AGGREGATION_URL = settings.AGGREGATION_URL


def handle_response(response):
    status_code = response.status_code
    detail = None
    error = None
    message = None
    try:
        response_json = response.json()
        detail = response_json.get("detail")
        error = response_json.get("error")
        message = response_json.get("message")
    except Exception:
        pass
    if error:
        return status_code, detail, error
    else:
        return status_code, detail, message


def template_path(name):
    return "frontend_app/" + str(name) + ".html"


def get_auth_token(request):
    return request.COOKIES.get("auth_token")


def get(url, auth_token=None):
    headers = None
    if auth_token:
        headers = {"Authorization": "JWT " + str(auth_token)}
    return requests.get(AGGREGATION_URL + url, headers=headers)


def post(url, request_json=None, auth_token=None):
    headers = None
    if auth_token:
        headers = {"Authorization": "JWT " + str(auth_token)}
    return requests.post(AGGREGATION_URL + url, json=request_json, headers=headers)


def put(url, request_json=None, auth_token=None):
    headers = None
    if auth_token:
        headers = {"Authorization": "JWT " + str(auth_token)}
    return requests.put(AGGREGATION_URL + url, json=request_json, headers=headers)


def login(username, password):
    reqest_json = {
        "username": username,
        "password": password,
    }
    return post("login/", request_json=reqest_json)


def logout(auth_token):
    return post("logout/", auth_token=auth_token)


def get_work_list():
    return get("work/")


def get_work(pk):
    return get("work/%s/" % str(pk))


def put_work(pk, title, course, semester, directions, auth_token):
    request_json = {
        "title": title,
        "course": course,
        "semester": semester,
        "directions": directions,
    }
    return put("work/%s/" % str(pk), request_json, auth_token)


def post_work(title, course, semester, directions, auth_token):
    request_json = {
        "title": title,
        "course": course,
        "semester": semester,
        "directions": directions,
    }
    return post("work/", request_json, auth_token)


def context_work(title=None, course=None, semester=None, directions=None, error_detail=None):
    directions = directions or []
    directions_response = get_direction_list()
    directions_response_json = directions_response.json()
    all_directions = directions_response_json.get("detail", [])
    selected_directions = []
    unselected_directions = []
    directions_id = []
    for d in directions:
        if isinstance(d, dict):
            directions_id.append(str(d.get("id")))
        else:
            directions_id.append(str(d))
    for d in all_directions:
        if str(d.get("id")) not in directions_id:
            unselected_directions.append(d)
        else:
            selected_directions.append(d)
    context = {
        "title": title or "",
        "course": course or "1",
        "semester": semester or "1",
        "directions": selected_directions,
        "courses": COURSES,
        "semesters": SEMESTERS,
        "unselected_directions": unselected_directions,
    }
    if error_detail:
        error_detail = error_detail.items()
        for field, error in error_detail:
            context[field + "_error"] = ""
            if isinstance(error, list):
                for er in error:
                    context[field + "_error"] += er + "  "
            else:
                context[field + "_error"] += error
    return context


def get_direction_list():
    return get("direction/")


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
                  status=status,
                  context={
                      "status_code": status,
                      "error_description": message})


def catch_exceptions(cookies=True):
    def dec_wrapper(func):
        def wrapper(self, request, *args, **kwargs):
            try:
                if cookies and not check_cookies(request):
                    response = redirect("login")
                    delete_cookies(response)
                    return response
                return func(self, request, *args, **kwargs)
            except ConnectionError:
                return page_error(request, 503, SERVICE_UNAVAILABLE)
            except Exception:
                return page_error(request, 500, INTERNAL_ERROR)
        return wrapper
    return dec_wrapper
