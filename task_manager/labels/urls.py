from django.urls import path

from . import views

app_name = 'task_manager.labels'

urlpatterns = [
    path('', views.LabelsView.as_view(), name='labels'),
    path('create/', views.CreateLabelView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateLabelView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete'),
]
