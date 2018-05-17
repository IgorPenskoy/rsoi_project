from numpy import zeros
from numpy import subtract
from random import SystemRandom

from scipy.optimize import linear_sum_assignment

from .models import Work
from .models import Student
from .models import Mentor
from .models import Distribution
from .constants import SCIENCE_MATCH
from .constants import PERSONAL_MATCH


def distribution_auto(work_id, group):
    print(u"LAUNCH AUTO DISTRIBUTION ON WORK %s GROUP %s" % (work_id, group))

    directions = Work.objects.get(pk=int(work_id)).directions.all()
    students = list(Student.objects.filter(group=group))
    mentors = list(Mentor.objects.all())
    students_count = len(students)
    mentors_count = len(mentors)

    if students_count > mentors_count:
        mentors.extend(SystemRandom().sample(mentors, students_count - mentors_count))
        mentors_count = len(mentors)

    mentors_science_preferences = []
    mentors_personal_preferences = []
    for mentor in mentors:
        mentors_science_preferences.append(mentor.science_preferences.all())
        mentors_personal_preferences.append(mentor.personal_preferences.all())
    students_science_preferences = []
    students_personal_preferences = []
    for student in students:
        students_science_preferences.append(student.science_preferences.all())
        students_personal_preferences.append(student.personal_preferences.all())

    cost_matrix = zeros((students_count, mentors_count))

    for i in range(students_count):
        for j in range(mentors_count):
            match = len(set(students_science_preferences[i]).
                        intersection(mentors_science_preferences[j]).
                        intersection(directions)) * SCIENCE_MATCH
            if students[i] in mentors_personal_preferences[j]:
                match += PERSONAL_MATCH
            if mentors[j] in students_personal_preferences[i]:
                match += PERSONAL_MATCH

            cost_matrix[i][j] = match

    cost_matrix = subtract(cost_matrix.max(), cost_matrix)
    students_idx, mentors_idx = linear_sum_assignment(cost_matrix)

    for i in students_idx:
        Distribution.objects.update_or_create(work_id=work_id,
                                              student=students[i],
                                              defaults={"mentor": mentors[mentors_idx[i]]})

    print(u"AUTO DISTRIBUTION DONE")
