from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('check/', views.AuthView.as_view(), name='check'),
    path('rest-auth/logout/', views.AuthLogoutView.as_view(), name='logout'),
    path('delete/<pk>/', views.DeleteUserView.as_view(), name='delete'),
    path('restore/<pk>/', views.RestoreUserView.as_view(), name='restore'),
]
