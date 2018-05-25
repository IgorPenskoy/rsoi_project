SERVICE_UNAVAILABLE = u"Сервис временно недоступен, попробуйте повторить действие позже"
INTERNAL_ERROR = u"Внутренняя ошибка сервера, попробуйте повторить действие похже"
NOT_FOUND = u"Запрашиваемый ресурс не найден"
FORBIDDEN = u"Нет прав доступа в этот раздел"
BAD_REQUEST = u"Некорректные данные"

COURSES = ["1", "2", "3", "4", "1М", "2М"]
SEMESTERS = ["1", "2"]

ADMIN_GROUP_NAME = "admin"

POSITION_CHOICES = [
    {"value": "AT", "view": u"Ассистент"},
    {"value": "TT", "view": u"Преподаватель"},
    {"value": "ST", "view": u"Старший преподаватель"},
    {"value": "AP", "view": u"Доцент"},
    {"value": "PP", "view": u"Профессор"},
]

TITLE_CHOICES = [
    {"value": "DT", "view": u"Доктор технических наук"},
    {"value": "CT", "view": u"Кандидат технических наук"},
    {"value": "DPHM", "view": u"Доктор физико-математических наук"},
    {"value": "CPHM", "view": u"Кандидат физико-математических наук"},
    {"value": "DE", "view": u"Доктор экономических наук"},
    {"value": "CE", "view": u"Кандидат экономических наук"},
    {"value": "DP", "view": u"Доктор педагогических наук"},
    {"value": "CP", "view": u"Кандидат педагогических наук"},
]

GROUPS = [str(i) + str(j) for i in range(1, 9) for j in range(1, 7)] +\
         [str(i) + str(j) + u"М" for i in range(1, 5) for j in range(1, 7)]
