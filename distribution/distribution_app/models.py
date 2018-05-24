from django.db import models

from .constants import GROUP_CHOICES
from .constants import INIT_GROUP
from .constants import POSITION_CHOICES
from .constants import TITLE_CHOICES
from .constants import TEACHER
from .constants import COURSE_CHOICES
from .constants import INIT_COURSE
from .constants import SEMESTER_CHOICES
from .constants import INIT_SEMESTER


from .error_messages import field_error_messages


class Direction(models.Model):
    title = models.CharField(
        max_length=500,
        unique=True,
        verbose_name=u"Название",
        error_messages=field_error_messages(
            unique=u"Направление с таким названием уже существует"
        )
    )

    class Meta:
        ordering = ('title',)


class Work(models.Model):
    title = models.CharField(
        max_length=500,
        unique=True,
        verbose_name=u"Название",
        error_messages=field_error_messages(
            unique=u"Работа с таким названием уже существует"
        )
    )
    course = models.CharField(
        max_length=2,
        choices=COURSE_CHOICES,
        default=INIT_COURSE,
        verbose_name=u"Курс",
        error_messages=field_error_messages(),
    )
    semester = models.CharField(
        max_length=1,
        choices=SEMESTER_CHOICES,
        default=INIT_SEMESTER,
        verbose_name=u"Семестр",
        error_messages=field_error_messages(),
    )
    directions = models.ManyToManyField(
        Direction,
        blank=True,
        verbose_name=u"Направления",
        error_messages=field_error_messages(),
    )

    class Meta:
        ordering = ('title',)


class Mentor(models.Model):
    surname = models.CharField(max_length=150, verbose_name=u"Фамилия")
    name = models.CharField(max_length=150, verbose_name=u"Имя")
    patronymic = models.CharField(max_length=150, verbose_name=u"Отчество")
    position = models.CharField(
        max_length=2,
        choices=POSITION_CHOICES,
        default=TEACHER,
        verbose_name=u"Должность"
    )
    title = models.CharField(
        max_length=4,
        choices=TITLE_CHOICES,
        blank=True,
        verbose_name=u"Звание"
    )
    email = models.EmailField(blank=True, null=True, verbose_name=u"Электронная почта")
    science_preferences = models.ManyToManyField(Direction, blank=True,
                                                 verbose_name=u"Научные предпочтения")
    personal_preferences = models.ManyToManyField("Student", blank=True,
                                                  verbose_name=u"Личные предпочтения")
    description = models.CharField(max_length=1000, blank=True, null=True,
                                   verbose_name=u"Информация")

    class Meta:
        ordering = ('surname', 'name', 'patronymic',)


class Student(models.Model):
    surname = models.CharField(max_length=150, verbose_name=u"Фамилия")
    name = models.CharField(max_length=150, verbose_name=u"Имя")
    patronymic = models.CharField(max_length=150, verbose_name=u"Отчество")
    group = models.CharField(
        max_length=3,
        choices=GROUP_CHOICES,
        default=INIT_GROUP,
        verbose_name=u"Группа"
    )
    email = models.EmailField(blank=True, null=True, verbose_name=u"Электронная почта")
    science_preferences = models.ManyToManyField(Direction, blank=True,
                                                 verbose_name=u"Научные предпочтения")
    personal_preferences = models.ManyToManyField(Mentor, blank=True,
                                                  verbose_name=u"Личные предпочтения")

    class Meta:
        ordering = ('group', 'surname', 'name', 'patronymic',)


class Distribution(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('work', 'student',)
        ordering = ('work__title', 'student__group', 'student__surname',
                    'student__name', 'student__patronymic',)
