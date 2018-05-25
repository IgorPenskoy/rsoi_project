from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('repository/create/', views.RepositoryCreateView.as_view(), name='repository_create'),
    path('repository/<pk>/', views.RepositoryDetailView.as_view(), name='repository_detail'),
]
