from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Direction
from .models import Work
from .models import Mentor
from .models import Student
from .serializers import DirectionSerializer
from .serializers import WorkSerializer
from .serializers import MentorSerializer
from .serializers import StudentSerializer


class IndexView(APIView):
    def get(self, request):
        return Response("DISTRIBUTION SERVICE")


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
