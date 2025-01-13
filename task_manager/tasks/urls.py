from django.urls import path
from . import views

app_name = 'task_manager.tasks'

urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='detail')
]
