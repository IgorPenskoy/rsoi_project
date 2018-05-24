from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('check/', views.AuthView.as_view(), name='check'),
    path('rest-auth/logout/', views.AuthLogoutView.as_view(), name='logout'),
    path('delete/<pk>/', views.DeleteUserView.as_view(), name='delete'),
    path('restore/<pk>/', views.RestoreUserView.as_view(), name='restore'),
    path('check/can_add_direction/', views.CanAddDirection.as_view(), name='check_can_add_direction'),
    path('check/can_add_mentor/', views.CanAddMentor.as_view(), name='check_can_add_mentor'),
    path('check/can_add_repository/', views.CanAddRepository.as_view(), name='check_can_add_repository'),
    path('check/can_add_student/', views.CanAddStudent.as_view(), name='check_can_add_student'),
    path('check/can_add_work/', views.CanAddWork.as_view(), name='check_can_add_work'),
    path('check/can_delete_direction/', views.CanDeleteDirection.as_view(),
         name='check_can_delete_direction'),
    path('check/can_delete_user/', views.CanDeleteUser.as_view(), name='check_can_delete_user'),
    path('check/can_delete_work/', views.CanDeleteWork.as_view(), name='check_can_delete_work'),
    path('check/can_edit_distribution/', views.CanEditDistribution.as_view(),
         name='check_can_edit_distribution'),
    path('check/can_edit_mentor_info/<pk>/', views.CanEditMentorInfo.as_view(),
         name='check_can_edit_mentor_info'),
    path('check/can_edit_student_info/<pk>/', views.CanEditStudentInfo.as_view(),
         name='check_can_edit_student_info'),
    path('check/can_edit_work/', views.CanEditWork.as_view(), name='check_can_edit_work'),
    path('check/can_edit_direction/', views.CanEditDirection.as_view(), name='check_can_edit_direction'),
    path('check/can_make_distribution/', views.CanMakeDistribution.as_view(),
         name='check_can_make_distribution'),
    path('check/can_watch_student_info/<pk>/', views.CanWatchStudentInfo.as_view(),
         name='check_can_watch_student_info'),
    path('check/can_watch_student_list/', views.CanWatchStudentList.as_view(),
         name='check_can_watch_student_list'),
]
