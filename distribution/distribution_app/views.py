from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError

from .models import Direction
from .models import Work
from .models import Mentor
from .models import Student
from .models import Distribution
from .serializers import DirectionSerializer
from .serializers import WorkSerializer
from .serializers import MentorSerializer
from .serializers import StudentSerializer
from .serializers import DistributionSerializer
from .functions import distribution_auto


class IndexView(APIView):
    def get(self, request):
        return Response()


class DirectionListView(ListCreateAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class DirectionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class WorkListView(ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class WorkDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class MentorListView(ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class MentorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class StudentListView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentByGroupView(ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        group = self.kwargs.get("group")
        return Student.objects.filter(group=group)


class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DistributionListView(ListCreateAPIView):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionGetView(ListAPIView):
    serializer_class = DistributionSerializer

    def get_queryset(self):
        work_id = self.kwargs.get("work_id")
        group = self.kwargs.get("group")
        return Distribution.objects.filter(work_id=work_id, student__group=group)


class DistributionAutoView(APIView):
    def post(self, request, work_id, group):
        try:
            distribution_auto(work_id, group)
        except Work.DoesNotExist:
            raise NotFound
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        except Exception:
            raise ValidationError(detail=u"Некорректные входные данные")
        return Response(u"Распределение успешно сформировано")
