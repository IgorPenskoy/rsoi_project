from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.AuthView.as_view(), name='check'),
]
