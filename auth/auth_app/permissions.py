STUDENT_PERMISSIONS = {
    ("can_add_repository", u"Создание репозитория"),
}

MENTOR_PERMISSIONS = {
    ("can_add_direction", u"Добавление нового направления"),
    ("can_edit_direction", u"Редактирование информации о направлении"),
    ("can_delete_direction", u"Удаление направления"),
    ("can_edit_work", u"Редактирование информации о работе"),
    ("can_watch_student_list", u"Просмотр списка студентов"),
    ("can_watch_student_info", u"Просмотр информации о студенте"),
}

ADMIN_PERMISSIONS = {
    ("can_add_mentor", u"Регистрация пользователя в роли руководителя"),
    ("can_add_student", u"Регистрация пользователя в роли студента"),
    ("can_edit_student_info", u"Редактирование информации о студенте"),
    ("can_edit_mentor_info", u"Редактирование информации о руководителе"),
    ("can_delete_user", u"Удаление пользователя"),
    ("can_edit_distribution", u"Редактирование информации о текущем распределении"),
    ("can_make_distribution", u"Запуск формирования нового распределения"),
    ("can_add_work", u"Добавление новой работы"),
    ("can_delete_work", u"Удаление работы"),
}
