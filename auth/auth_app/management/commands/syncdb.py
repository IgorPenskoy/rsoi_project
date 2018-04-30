import string
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from django.contrib.auth.models import User

from auth_app.permissions import STUDENT_PERMISSIONS
from auth_app.permissions import MENTOR_PERMISSIONS
from auth_app.permissions import ADMIN_PERMISSIONS
from auth_app.constants import ADMIN_USERNAME
from auth_app.constants import ADMIN_EMAIL
from auth_app.constants import MENTOR_GROUP_NAME
from auth_app.constants import STUDENT_GROUP_NAME
from auth_app.constants import PERMISSION_MODEL_NAME
from auth_app.constants import APP_LABEL


def password_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def create_permissions(permissions_set, content_type):
    permissions = []
    for codename, name in permissions_set:
        permission, _ = Permission.objects.update_or_create(codename=codename,
                                                            content_type=content_type,
                                                            defaults={"name": name})
        permissions.append(permission)
    return permissions


def add_permissions_to_group(group, permissions):
    for permission in permissions:
        group.permissions.add(permission)


class Command(BaseCommand):
    help = "Создать группы и права"

    def write_out(self, text):
        self.stdout.write(text)

    def write_out_success(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def handle(self, *args, **options):

        mentor_group, _ = Group.objects.get_or_create(name=MENTOR_GROUP_NAME)
        student_group, _ = Group.objects.get_or_create(name=STUDENT_GROUP_NAME)

        ct, _ = ContentType.objects.get_or_create(model=PERMISSION_MODEL_NAME,
                                                  app_label=APP_LABEL)

        student_permissions = create_permissions(STUDENT_PERMISSIONS, ct)
        add_permissions_to_group(student_group, student_permissions)

        mentor_permissions = create_permissions(MENTOR_PERMISSIONS, ct)
        add_permissions_to_group(mentor_group, mentor_permissions)

        create_permissions(ADMIN_PERMISSIONS, ct)

        for group in Group.objects.all():
            for permission in group.permissions.all().order_by():
                self.write_out_success("К группе %s добавлено право %s"
                                       % (group.name, permission.name))
            self.write_out("\n")

        try:
            User.objects.get(username=ADMIN_USERNAME)
        except User.DoesNotExist:
            password = User.objects.make_random_password()
            admin = User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, password)
            self.write_out_success("Создан адмнистратор %s с паролем %s\n"
                                   % (admin.username, password))

        self.write_out_success("Создание групп и прав завершено")
