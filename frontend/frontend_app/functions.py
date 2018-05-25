import requests

from requests.exceptions import ConnectionError
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect

from .constants import SERVICE_UNAVAILABLE
from .constants import INTERNAL_ERROR
from .constants import COURSES
from .constants import SEMESTERS
from .constants import POSITION_CHOICES
from .constants import TITLE_CHOICES
from .constants import GROUPS

AGGREGATION_URL = settings.AGGREGATION_URL


#########################################################################################


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


def error_context(context, error_detail):
    if error_detail:
        error_detail = error_detail.items()
        for field, error in error_detail:
            context[field + "_error"] = ""
            if isinstance(error, list):
                for er in error:
                    context[field + "_error"] += er + "\n"
            else:
                context[field + "_error"] += error
    return context


#########################################################################################


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


def delete(url, auth_token=None):
    headers = None
    if auth_token:
        headers = {"Authorization": "JWT " + str(auth_token)}
    return requests.delete(AGGREGATION_URL + url, headers=headers)


#########################################################################################


def login(username, password):
    reqest_json = {
        "username": username,
        "password": password,
    }
    return post("login/", request_json=reqest_json)


def logout(auth_token):
    return post("logout/", auth_token=auth_token)


#########################################################################################


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


def delete_work(pk, auth_token):
    return delete("work/%s/" % str(pk), auth_token)


def context_work(title=None, course=None, semester=None,
                 directions=None, error_detail=None, w_id=None):
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
        "id": w_id,
        "title": title or "",
        "course": course or "1",
        "semester": semester or "1",
        "directions": selected_directions,
        "courses": COURSES,
        "semesters": SEMESTERS,
        "unselected_directions": unselected_directions,
    }
    return error_context(context, error_detail)


#########################################################################################


def get_direction_list():
    return get("direction/")


def get_direction(pk):
    return get("direction/%s/" % str(pk))


def put_direction(pk, title, auth_token):
    request_json = {
        "title": title,
    }
    return put("direction/%s/" % str(pk), request_json, auth_token)


def post_direction(title, auth_token):
    request_json = {
        "title": title,
    }
    return post("direction/", request_json, auth_token)


def delete_direction(pk, auth_token):
    return delete("direction/%s/" % str(pk), auth_token)


def context_direction(title=None, error_detail=None, d_id=None):
    context = {
        "id": d_id,
        "title": title or "",
    }
    return error_context(context, error_detail)


#########################################################################################


def get_student_list():
    return get("student/")


def get_mentor_list():
    return get("mentor/")


def get_mentor(pk):
    return get("mentor/%s/" % str(pk))


def put_mentor(pk, surname, name, patronymic, position,
               title, email, sciences, personals, auth_token):
    request_json = {
        "id": pk,
        "surname": surname,
        "name": name,
        "patronymic": patronymic,
        "position": position,
        "title": title,
        "email": email,
        "science_preferences": sciences,
        "personal_preferences": personals,
    }
    return put("mentor/%s/" % str(pk), request_json, auth_token)


def post_mentor(surname, name, patronymic, position,
                title, email, auth_token):
    request_json = {
        "surname": surname,
        "name": name,
        "patronymic": patronymic,
        "position": position,
        "title": title,
        "email": email,
    }
    return post("register_mentor/", request_json, auth_token)


def delete_mentor(pk, auth_token):
    return delete("delete_mentor/%s/" % str(pk), auth_token)


def context_mentor(surname=None, name=None, patronymic=None, position=None, title=None,
                   email=None, sciences=None, personals=None,
                   error_detail=None, m_id=None):
    sciences = sciences or []
    directions_response = get_direction_list()
    directions_response_json = directions_response.json()
    all_directions = directions_response_json.get("detail", [])
    selected_directions = []
    unselected_directions = []
    directions_id = []
    for d in sciences:
        if isinstance(d, dict):
            directions_id.append(str(d.get("id")))
        else:
            directions_id.append(str(d))
    for d in all_directions:
        if str(d.get("id")) not in directions_id:
            unselected_directions.append(d)
        else:
            selected_directions.append(d)

    personals = personals or []
    students_response = get_student_list()
    students_response_json = students_response.json()
    all_students = students_response_json.get("detail", [])
    selected_students = []
    unselected_students = []
    students_id = []
    for d in personals:
        if isinstance(d, dict):
            students_id.append(str(d.get("id")))
        else:
            students_id.append(str(d))
    for d in all_students:
        if str(d.get("id")) not in students_id:
            unselected_students.append(d)
        else:
            selected_students.append(d)

    context = {
        "id": m_id,
        "name": name or "",
        "surname": surname or "",
        "patronymic": patronymic or "",
        "position": position or u"Преподаватель",
        "title": title or "",
        "email": email or "",
        "sciences": selected_directions,
        "unselected_sciences": unselected_directions,
        "personals": selected_students,
        "unselected_personals": unselected_students,
        "positions": POSITION_CHOICES,
        "titles": TITLE_CHOICES,
    }
    return error_context(context, error_detail)


#########################################################################################


def get_student(pk):
    return get("student/%s/" % str(pk))


def put_student(pk, surname, name, patronymic, group,
                email, sciences, personals, auth_token):
    request_json = {
        "id": pk,
        "surname": surname,
        "name": name,
        "patronymic": patronymic,
        "group": group,
        "email": email,
        "science_preferences": sciences,
        "personal_preferences": personals,
    }
    return put("student/%s/" % str(pk), request_json, auth_token)


def post_student(surname, name, patronymic, group, email, auth_token):
    request_json = {
        "surname": surname,
        "name": name,
        "patronymic": patronymic,
        "group": group,
        "email": email,
    }
    return post("register_student/", request_json, auth_token)


def delete_student(pk, auth_token):
    return delete("delete_student/%s/" % str(pk), auth_token)


def context_student(surname=None, name=None, patronymic=None, group=None, email=None,
                    sciences=None, personals=None, error_detail=None, s_id=None):
    sciences = sciences or []
    directions_response = get_direction_list()
    directions_response_json = directions_response.json()
    all_directions = directions_response_json.get("detail", [])
    selected_directions = []
    unselected_directions = []
    directions_id = []
    for d in sciences:
        if isinstance(d, dict):
            directions_id.append(str(d.get("id")))
        else:
            directions_id.append(str(d))
    for d in all_directions:
        if str(d.get("id")) not in directions_id:
            unselected_directions.append(d)
        else:
            selected_directions.append(d)

    personals = personals or []
    mentors_response = get_mentor_list()
    mentors_response_json = mentors_response.json()
    all_mentors = mentors_response_json.get("detail", [])
    selected_mentors = []
    unselected_mentors = []
    mentors_id = []
    for d in personals:
        if isinstance(d, dict):
            mentors_id.append(str(d.get("id")))
        else:
            mentors_id.append(str(d))
    for d in all_mentors:
        if str(d.get("id")) not in mentors_id:
            unselected_mentors.append(d)
        else:
            selected_mentors.append(d)

    context = {
        "id": s_id,
        "name": name or "",
        "surname": surname or "",
        "patronymic": patronymic or "",
        "group": group,
        "email": email or "",
        "sciences": selected_directions,
        "unselected_sciences": unselected_directions,
        "personals": selected_mentors,
        "unselected_personals": unselected_mentors,
        "groups": GROUPS,
    }
    return error_context(context, error_detail)


#########################################################################################


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


#########################################################################################


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
