STUDENT_GROUP = "student"
MENTOR_GROUP = "mentor"
LOGIN_ERROR = u"Неверные логин и/или пароль"
AUTH_ERROR = u"Необходимо войти в систему"
SUCCESS_LOGOUT = u"Вы успешно вышли из системы"
NOT_FOUND_ERROR = u"Запрашиваемый ресурс не найден"
PERMISSION_DENIED_ERROR = u"Недостаточно прав для доступа к данному ресурсу"
JSON_ERROR = u"Неверный формат JSON"
NOT_ALLOWED_ERROR = u"Недопустимая операция"
NOT_ACCEPTABLE_ERROR = u"Недопустимый тип запрашиваемого ресурса"
UNSUPPORTED_MEDIA_ERROR = u"Недопустимый тип входных данных"
THROTTLED_ERROR = u"Сервер перегружен, попробуйте повторить действие позже"
VALIDATION_ERROR = u"Некорректные входные данные"
MANDATORY_FIELD = u"Это поле обязательно"
NOT_EMPTY_FIELD = u"Это поле не может быть пустым"
NAME_RE = {
    "re": r"^[А-Яа-я]+$",
    "message": u"Имя, фамилия и отчество могут содержать только русские буквы",
}
WORK_RE = {
    "re": r"^[А-Яа-я ]+$",
    "message": u"Наименование может содержать только русские буквы и пробелы",
}
SUCCESS_REGISTRATION = u"Пользователь зарегистрирован"
SUCCESS_DELETE = u"Пользователь удален"
