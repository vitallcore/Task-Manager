from django.urls import path

from task_manager.statuses.views import (StatusListView,
                                         StatusCreateView,
                                         StatusDeleteView,
                                         StatusUpdateView)

urlpatterns = [
    path('', StatusListView.as_view(), name='status_list'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update')
]
