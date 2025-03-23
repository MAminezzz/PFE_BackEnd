from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Le formulaire est valide.")  
            Utilisateur.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                gender=form.cleaned_data['gender'],
                is_confirmed=True  
            )
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
        else:
            print("Le formulaire n'est pas valide.") 
            print(form.errors)  
            messages.error(request, 'Erreur lors de l\'inscription. Veuillez vérifier les champs.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = Utilisateur.objects.filter(username=username, password=password).first()
        if user:
            return redirect('welcome', username=user.username)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'users/login.html')
    return render(request, 'users/login.html')
def welcome(request, username):
    if request.method == "POST":
        image = request.FILES.get('image')
        upper_clothes = request.POST.get('upper_clothes')
        lower_clothes = request.POST.get('lower_clothes')        
        return render(request, 'users/welcome.html', {
            'username': username,
            'upper_clothes': upper_clothes,
            'lower_clothes': lower_clothes,
        })
    
    return render(request, 'users/welcome.html', {'username': username})