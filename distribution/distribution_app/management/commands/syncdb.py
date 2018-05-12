import random

from django.core.management.base import BaseCommand
from django_dynamic_fixture import G

from distribution_app.models import Work
from distribution_app.models import Direction
from distribution_app.models import Student
from distribution_app.models import Mentor


class Command(BaseCommand):
    help = "Генерация тестовых данных"

    def write_out(self, text):
        self.stdout.write(text)

    def write_out_success(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def handle(self, *args, **options):

        directions = []
        for i in range(20):
            direction = G(Direction)
            directions.append(direction)

        work = G(Work)
        work.directions.set(directions)

        secure_random = random.SystemRandom()
        students = []
        for i in range(20):
            student = G(Student)
            student.science_preferences.set(secure_random.sample(directions, 5))
            students.append(student)

        mentors = []
        for i in range(20):
            mentor = G(Mentor)
            mentor.science_preferences.set(secure_random.sample(directions, 5))
            mentors.append(mentor)

        for mentor in mentors:
            mentor.personal_preferences.set(secure_random.sample(students,
                                                                 secure_random.randint(0, 4)))

        for student in students:
            student.personal_preferences.set(secure_random.sample(mentors,
                                                                  secure_random.randint(0, 4)))
