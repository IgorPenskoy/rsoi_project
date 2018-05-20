from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register_student/', views.RegistrationStudentView.as_view(), name='register_student'),
    path('register_mentor/', views.RegistrationMentorView.as_view(), name='register_mentor'),
    path('delete_student/<pk>/', views.DeleteStudentView.as_view(), name='delete_student'),
    path('delete_mentor/<pk>/', views.DeleteMentorView.as_view(), name='delete_mentor'),
]
