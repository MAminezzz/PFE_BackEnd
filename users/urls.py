from django.urls import path
from .views import register, login_view, welcome, upload_images, outfit_generation

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),  # URL simplifiée (sans username)
    path('welcome/<str:username>/', welcome, name='welcome'),
    path('upload/', upload_images, name='upload_images'),
    path('outfit-generation/', outfit_generation, name='outfit_generation'),
]