from django.urls import path
from .views import register, login_view, welcome

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('welcome/<str:username>/', welcome, name='welcome'),
]