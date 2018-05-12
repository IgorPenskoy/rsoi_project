from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('direction/', views.DirectionListView.as_view(), name='direction_list'),
    path('direction/<pk>/', views.DirectionDetailView.as_view(), name='direction_detail'),
    path('work/', views.WorkListView.as_view(), name='work_list'),
    path('work/<pk>/', views.WorkDetailView.as_view(), name='work_detail'),
    path('mentor/', views.MentorListView.as_view(), name='mentor_list'),
    path('mentor/<pk>/', views.MentorDetailView.as_view(), name='mentor_detail'),
    path('student/', views.StudentListView.as_view(), name='student_list'),
    path('student/group/<str:group>/', views.StudentByGroupView.as_view(), name='student_by_group'),
    path('student/<pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('distribution/', views.DistributionListView.as_view(), name='distribution_list'),
    path('distribution/auto/<int:work_id>/<str:group>/', views.DistributionAutoView.as_view(),
         name='distribution_auto'),
    path('distribution/<pk>/', views.DistributionDetailView.as_view(), name='distribution_detail'),
]
