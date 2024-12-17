from django.urls import path
from .views import (
    ProjectListView,
    ProjectCreateView,
    TaskCreateView,
    TaskCompleteView,
    ObtainTokenView,
)

app_name = 'projects_api'

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path(
        'task/<int:task_id>/complete/', TaskCompleteView.as_view(), name='task_complete'
    ),
    path('token/', ObtainTokenView.as_view(), name='token_obtain'),
]
