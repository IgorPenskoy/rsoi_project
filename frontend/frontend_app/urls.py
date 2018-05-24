from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('work/', views.WorkListView.as_view(), name='work_list'),
    path('work/new/', views.WorkNewView.as_view(), name='work_new'),
    path('work/<pk>/', views.WorkDetailView.as_view(), name='work_detail'),
]
