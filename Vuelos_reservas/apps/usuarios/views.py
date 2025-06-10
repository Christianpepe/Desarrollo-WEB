from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('ingreso')  # Redirige a inicio después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def ingreso(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '¡Ingreso exitoso!')
            return redirect('inicio')  # Redirige a inicio después de loguear
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/ingreso.html', {'form': form})

@login_required
def inicio(request):
    return render(request, 'inicio.html')

def salir(request):
    logout(request)
    return redirect('ingreso')  # O la página que quieras después de cerrar sesión
