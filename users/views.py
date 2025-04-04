from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Utilisateur, ClothUpload, GeneratedOutfit
from .forms import RegisterForm
import requests
import json
import os
from django.conf import settings
from django.core.files.base import ContentFile
import base64
from urllib.parse import urlparse
from urllib.request import urlretrieve
import tempfile

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome', username=user.username)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'users/login.html')

@login_required
def upload_images(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        if not images:
            messages.error(request, 'Aucune image sélectionnée')
            return redirect('welcome', username=request.user.username)
        
        successful_uploads = 0
        for img in images:
            if img.size > 5 * 1024 * 1024:  # 5MB max
                messages.warning(request, f"L'image {img.name} est trop volumineuse (max 5MB)")
                continue
                
            # Create the upload directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', f'user_{request.user.id}')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the image
            cloth_upload = ClothUpload.objects.create(
                user=request.user,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                image=img
            )
            successful_uploads += 1
        
        if successful_uploads > 0:
            messages.success(request, f'{successful_uploads} image(s) uploadée(s) avec succès!')
        return redirect('welcome', username=request.user.username)
    return render(request, 'users/welcome.html')

@login_required
def welcome(request, username):
    try:
        user = Utilisateur.objects.get(username=username)
        if user != request.user:
            raise PermissionDenied
        uploads = user.cloth_uploads.all().order_by('-upload_date')
        generated_outfits = user.generated_outfits.all().order_by('-generation_date')
        return render(request, 'users/welcome.html', {
            'user': user, 
            'uploads': uploads,
            'generated_outfits': generated_outfits
        })
    except Utilisateur.DoesNotExist:
        messages.error(request, "Utilisateur non trouvé")
        return redirect('home')

@login_required
def outfit_generation(request):
    if request.method == "POST":
        event_type = request.POST.get('event_type')
        if not event_type:
            messages.error(request, "Veuillez sélectionner un type d'événement")
            return redirect('outfit_generation')
        
        try:
            # Create the directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'generated_outfits', f'user_{request.user.id}')
            os.makedirs(upload_dir, exist_ok=True)

            # Create the generated outfit record
            generated_outfit = GeneratedOutfit.objects.create(
                user=request.user,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                event_type=event_type
            )
            
            # Use a local file instead of downloading
            default_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default_outfit.jpg')
            
            # Save the image
            image_name = f'outfit_{event_type}_{generated_outfit.id}.jpg'
            with open(default_image_path, 'rb') as img_file:
                generated_outfit.image.save(
                    image_name,
                    ContentFile(img_file.read()),
                    save=True
                )
            
            messages.success(request, "Tenue générée avec succès!")
            return render(request, 'users/outfit_generation.html', {
                'generated_image': generated_outfit.image.url,
                'event_type': event_type
            })
            
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la génération de la tenue: {str(e)}")
            return redirect('outfit_generation')
            
    return render(request, 'users/outfit_generation.html')