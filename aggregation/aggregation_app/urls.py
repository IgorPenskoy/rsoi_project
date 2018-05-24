from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('student/', views.ListStudentView.as_view(), name='student_list'),
    path('student/group/<str:group>/', views.ListStudentByGroupView.as_view(), name='student_list'),
    path('mentor/', views.ListMentorView.as_view(), name='mentor_list'),
    path('student/<pk>/', views.StudentView.as_view(), name='student'),
    path('mentor/<pk>/', views.MentorView.as_view(), name='mentor'),
    path('register_student/', views.RegistrationStudentView.as_view(), name='register_student'),
    path('register_mentor/', views.RegistrationMentorView.as_view(), name='register_mentor'),
    path('delete_student/<pk>/', views.DeleteStudentView.as_view(), name='delete_student'),
    path('delete_mentor/<pk>/', views.DeleteMentorView.as_view(), name='delete_mentor'),
    path('work/', views.WorkListView.as_view(), name='work_list'),
    path('work/<pk>/', views.WorkView.as_view(), name='work_detail'),
    path('direction/', views.DirectionListView.as_view(), name='direction_list'),
    path('direction/<pk>/', views.DirectionView.as_view(), name='direction_detail'),
    path('distribution/work/<int:work_id>/group/<str:group>/', views.DistributionListView.as_view(),
         name='distribution_list'),
    path('distribution/<pk>/', views.DistributionView.as_view(), name='distribution_detail'),
    path('repository/<int:user_id>/', views.RepositoryView.as_view(), name='repository'),
]
