from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('students_by_group/<str:group>/', views.ListStudentView.as_view(), name='students_by_group'),
    path('mentors/', views.ListMentorView.as_view(), name='mentor_list'),
    path('student/<pk>/', views.StudentView.as_view(), name='student'),
    path('mentor/<pk>/', views.MentorView.as_view(), name='mentor'),
    path('register_student/', views.RegistrationStudentView.as_view(), name='register_student'),
    path('register_mentor/', views.RegistrationMentorView.as_view(), name='register_mentor'),
    path('delete_student/<pk>/', views.DeleteStudentView.as_view(), name='delete_student'),
    path('delete_mentor/<pk>/', views.DeleteMentorView.as_view(), name='delete_mentor'),
]
