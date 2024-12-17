from django.urls import path

from . import views
from .views import register, UserLoginView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.confirm_logout, name='logout'),
]
