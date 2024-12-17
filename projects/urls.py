from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/complete/', views.task_complete, name='task_complete'),
]
