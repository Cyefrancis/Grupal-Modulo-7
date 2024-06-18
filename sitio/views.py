from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a alguna página de éxito o a la página de inicio
            return redirect('iniciar_sesion')
    else:
        form = UserCreationForm()
    return render(request, 'registro_usuario.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard or any other page after login
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    # Your dashboard view logic here
    return render(request, 'dashboard.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('home') 