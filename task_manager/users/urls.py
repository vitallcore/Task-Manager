from django.urls import path

from task_manager.users.views import (UserListView,
                                      UserCreateView,
                                      UserDeleteView,
                                      UserUpdateView)

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update')
]
