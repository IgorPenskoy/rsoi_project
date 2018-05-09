from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField

from .models import Direction
from .models import Work
from .models import Mentor
from .models import Student


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
