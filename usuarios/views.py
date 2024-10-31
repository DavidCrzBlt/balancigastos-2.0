from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Profile

from .forms import ProfileForm, UserRegisterForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('usuarios:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'usuarios/signup.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/profile.html', {'username': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('usuarios:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'usuarios/edit_profile.html', {'username': profile,'form':form})

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')
