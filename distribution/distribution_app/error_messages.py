def field_error_messages(null=None, blank=None, invalid=None, invalid_choice=None,
                         unique=None, unique_for_date=None):
    error_messages = {
        "null": null or u"Это поле обязательно",
        "blank": blank or u"Это поле не может быть пустым",
        "invalid": invalid or u"Некорректные данные",
        "invalid_choice": invalid_choice or u"Недопустимый выбор",
        "unique": unique or u"Это поле не должно повторяться",
        "unique_for_date": unique_for_date or u"Это поле не должно "
                                              u"повторяться совместно с датой",
    }

    return error_messages
