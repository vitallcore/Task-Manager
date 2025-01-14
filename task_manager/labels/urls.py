from django.urls import path

from task_manager.labels.views import (LabelListView,
                                       LabelCreateView,
                                       LabelDeleteView,
                                       LabelUpdateView)

urlpatterns = [
    path('', LabelListView.as_view(), name='label_list'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='label_delete'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='label_update')
]
