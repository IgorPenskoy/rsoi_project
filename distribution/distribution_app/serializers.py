from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField

from .models import Direction
from .models import Work
from .models import Mentor
from .models import Student
from .models import Distribution


class DirectionSerializer(ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'title',)


class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'title', 'course', 'semester', 'directions',)


class MentorSerializer(ModelSerializer):
    id = IntegerField()

    class Meta:
        model = Mentor
        fields = ('id', 'surname', 'name', 'patronymic', 'position', 'title',
                  'email', 'science_preferences', 'personal_preferences', 'description')


class StudentSerializer(ModelSerializer):
    id = IntegerField()

    class Meta:
        model = Student
        fields = ('id', 'surname', 'name', 'patronymic', 'group', 'email',
                  'science_preferences', 'personal_preferences',)


class DistributionSerializer(ModelSerializer):
    def to_representation(self, instance):
        representation = dict()

        representation["id"] = instance.id
        representation["work_id"] = instance.work.id
        representation["student_id"] = instance.student.id
        representation["mentor_id"] = instance.mentor.id

        representation["work"] = instance.work.title
        representation["student"] = "%s %s. %s." % (instance.student.surname,
                                                    instance.student.name[0],
                                                    instance.student.patronymic[0])
        representation["mentor"] = "%s %s. %s." % (instance.mentor.surname,
                                                   instance.mentor.name[0],
                                                   instance.mentor.patronymic[0])
        representation["student_group"] = instance.student.group

        return representation

    class Meta:
        model = Distribution
        fields = ('id', 'work', 'student', 'mentor',)
