from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('work/', views.WorkListView.as_view(), name='work_list'),
    path('work/new/', views.WorkNewView.as_view(), name='work_new'),
    path('work/<pk>/', views.WorkDetailView.as_view(), name='work_detail'),
    path('direction/', views.DirectionListView.as_view(), name='direction_list'),
    path('direction/new/', views.DirectionNewView.as_view(), name='direction_new'),
    path('direction/<pk>/', views.DirectionDetailView.as_view(), name='direction_detail'),
    path('mentor/', views.MentorListView.as_view(), name='mentor_list'),
    path('mentor/new/', views.MentorNewView.as_view(), name='mentor_new'),
    path('mentor/<pk>/', views.MentorDetailView.as_view(), name='mentor_detail'),
    path('student/', views.StudentListView.as_view(), name='student_list'),
    path('student/new/', views.StudentNewView.as_view(), name='student_new'),
    path('student/<pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('repository/<pk>/', views.RepositoryView.as_view(), name='repository'),
]
