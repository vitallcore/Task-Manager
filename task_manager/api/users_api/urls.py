from django.urls import path
# from rest_framework import routers
from . import api_views

app_name = 'task_manager.api.users_api'

# users_router = routers.SimpleRouter()
# users_router.register(r'users', api_views.UsersApiViewSet)

urlpatterns = [
    path('users/', api_views.UsersAPIList.as_view(), name='users_api'),
    path('users/<int:pk>/', api_views.UsersAPIUpdateDestroy.as_view()),
]
