from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from account.decorators import role_required
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.permissions import BasePermission


# Кастомные права доступа для API
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'manager']


class IsUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role in ['admin', 'manager']


# Обычные представления для работы с проектами и задачами
@login_required
@role_required('ADMIN', 'MANAGER', 'USER')
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
@role_required('ADMIN', 'MANAGER')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
@role_required('USER', 'MANAGER', 'ADMIN')
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(
        request, 'projects/project_detail.html', {'project': project, 'tasks': tasks}
    )


@login_required
@role_required('MANAGER', 'ADMIN')
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(
        request, 'projects/task_form.html', {'form': form, 'project': project}
    )


@login_required
@role_required('USER', 'MANAGER', 'ADMIN')
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = True
    task.save()
    return redirect('project_detail', project_id=task.project.id)


class ProjectCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrManager]  # Доступ только для админов и менеджеров

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by=request.user
            )  # Связываем проект с текущим пользователем
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Создание проекта только для администраторов и менеджеров
        if request.user.role not in ['admin', 'manager']:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, *args, **kwargs):
        project = get_object_or_404(Project, id=project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class TaskCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrManager]  # Только администратор или менеджер

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCompleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOrReadOnly]

    def post(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, id=task_id)
        if task:
            task.is_completed = True
            task.save()
            return Response({"status": "task completed"})
        return Response({"error": "task not found"}, status=status.HTTP_404_NOT_FOUND)


class ObtainTokenView(APIView):
    permission_classes = [AllowAny]  # Разрешить доступ всем пользователям

    def post(self, request, *args, **kwargs):
        # Получаем данные пользователя из запроса
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Проверяем пароль
        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, status=400)

        # Создаем токен
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        )
