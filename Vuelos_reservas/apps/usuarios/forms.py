from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from hcaptcha.fields import hCaptchaField
#CORONA GARCIA CHRISTIAN JAVIER
class CustomUserCreationForm(UserCreationForm):
    hcaptcha = hCaptchaField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.prioridad = 0  
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    hcaptcha = hCaptchaField()
