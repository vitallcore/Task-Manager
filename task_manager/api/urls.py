from django.urls import include, path

app_name = 'task_manager.api'

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('task_manager.api.users_api.urls')),
]
