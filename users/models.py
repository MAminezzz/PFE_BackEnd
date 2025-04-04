from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.conf import settings

def user_image_path(instance, filename):
    # Cette ligne doit être indentée
    return os.path.join('uploads', f'user_{instance.user.id}', filename)

def generated_outfit_path(instance, filename):
    return os.path.join('generated_outfits', f'user_{instance.user.id}', filename)

class Utilisateur(AbstractUser):
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    is_confirmed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

class ClothUpload(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='cloth_uploads')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=user_image_path,
        help_text='Max 5MB file size'
    )
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.upload_date}"

class GeneratedOutfit(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='generated_outfits')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to=generated_outfit_path,
        help_text='Generated outfit image'
    )
    generation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event_type} - {self.generation_date}"