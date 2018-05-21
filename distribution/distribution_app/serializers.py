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
    directions_detail = DirectionSerializer(source="directions",
                                            many=True,
                                            read_only=True)

    class Meta:
        model = Work
        fields = ('id', 'title', 'course', 'semester', 'directions', 'directions_detail',)


class MentorForStudentSerializer(ModelSerializer):
    def to_representation(self, instance):
        representation = dict()

        representation["id"] = instance.id
        representation["name"] = "%s %s. %s." % (instance.surname,
                                                 instance.name[0],
                                                 instance.patronymic[0])

        return representation

    class Meta:
        model = Mentor
        fields = ('id', 'surname', 'name', 'patronymic',)


class StudentForMentorSerializer(ModelSerializer):
    def to_representation(self, instance):
        representation = dict()

        representation["id"] = instance.id
        representation["name"] = "%s %s. %s." % (instance.surname,
                                                 instance.name[0],
                                                 instance.patronymic[0])
        representation["group"] = instance.group

        return representation

    class Meta:
        model = Student
        fields = ('id', 'surname', 'name', 'patronymic', 'group')


class MentorSerializer(ModelSerializer):
    id = IntegerField()
    science_preferences_detail = DirectionSerializer(source="science_preferences",
                                                     many=True,
                                                     read_only=True)
    personal_preferences_detail = StudentForMentorSerializer(source="personal_preferences",
                                                             many=True,
                                                             read_only=True)

    class Meta:
        model = Mentor
        fields = ('id', 'surname', 'name', 'patronymic', 'position', 'title',
                  'email', 'science_preferences', 'personal_preferences', 'description',
                  'science_preferences_detail', 'personal_preferences_detail',)


class StudentSerializer(ModelSerializer):
    id = IntegerField()
    science_preferences_detail = DirectionSerializer(source="science_preferences",
                                                     many=True,
                                                     read_only=True)
    personal_preferences_detail = MentorForStudentSerializer(source="personal_preferences",
                                                             many=True,
                                                             read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'surname', 'name', 'patronymic', 'group', 'email',
                  'science_preferences', 'personal_preferences',
                  'science_preferences_detail', 'personal_preferences_detail',)


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
