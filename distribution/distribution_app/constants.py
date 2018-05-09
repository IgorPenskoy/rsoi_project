# Должность

ASSISTANT = "AT"
TEACHER = "TT"
SENIOR = "ST"
DOCENT = "AP"
PROFESSOR = "PP"

POSITION_CHOICES = (
    (ASSISTANT, u"Ассистент"),
    (TEACHER, u"Преподаватель"),
    (SENIOR, u"Старший преподаватель"),
    (DOCENT, u"Доцент"),
    (PROFESSOR, u"Профессор"),
)

# Звание

PHD_T = u"DT"
PHD_C_T = u"CT"
PHD_PHM = u"DPHM"
PHD_C_PHM = u"CPHM"
PHD_E = u"DE"
PHD_C_E = u"CE"
PHD_P = u"DP"
PHD_C_P = u"CP"

TITLE_CHOICES = (
    (PHD_T, u"Доктор технических наук"),
    (PHD_C_T, u"Кандидат технических наук"),
    (PHD_PHM, u"Доктор физико-математических наук"),
    (PHD_C_PHM, u"Кандидат физико-математических наук"),
    (PHD_E, u"Доктор экономических наук"),
    (PHD_C_E, u"Кандидат экономических наук"),
    (PHD_P, u"Доктор педагогических наук"),
    (PHD_C_P, u"Кандидат педагогических наук"),
)

# Группа

INIT_GROUP = "11"

GROUP_CHOICES = tuple(
    [(str(i) + str(j), u"ИУ7-%d%d" % (i, j)) for i in range(1, 9) for j in range(1, 7)] +
    [(str(i) + str(j) + u"М", u"ИУ7-%d%dМ" % (i, j)) for i in range(1, 5) for j in range(1, 7)]
)

# Курс

INIT_COURSE = "1"

COURSE_CHOICES = tuple(
    [(str(i), str(i)) for i in range(1, 5)] +
    [(str(i) + u"М", str(i) + u"М") for i in range(1, 3)]
)

# Семестр

INIT_SEMESTER = "1"

SEMESTER_CHOICES = tuple(
    [(str(i), str(i)) for i in range(1, 3)]
)
