from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CustomUser

# Aquí inicia tu código

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_picture']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
