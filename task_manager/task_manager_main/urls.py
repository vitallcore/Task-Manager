from django.urls import path

from . import views

app_name = 'task_manager_main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
