from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from hcaptcha.fields import hCaptchaField
#CORONA GARCIA CHRISTIAN JAVIER
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CustomUserCreationForm(UserCreationForm):
    # hcaptcha = hCaptchaField()  
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'telefono', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^\w+$', username):
            raise ValidationError('El nombre de usuario solo puede contener letras, números y guion bajo (_).')
        return username

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise ValidationError('El número de teléfono solo puede contener dígitos.')
        return telefono

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.match(r'^[A-Za-z0-9]+$', password1):
            raise ValidationError('La contraseña solo puede contener letras y números (sin caracteres especiales).')
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Introduce un correo electrónico válido.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.prioridad = 0          
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    # hcaptcha = hCaptchaField() 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'