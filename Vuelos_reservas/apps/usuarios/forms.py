from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'telefono', 'password1', 'password2')  # Quitar prioridad del formulario

    def save(self, commit=True):
        user = super().save(commit=False)
        user.prioridad = 0  # Siempre prioridad 0
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    pass  # Puedes usar el form por defecto sin cambios
