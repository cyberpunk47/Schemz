from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['login_count'] = request.session.get('login_count', 0) + 1
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            response = redirect('home')
            response.set_cookie('last_user', user.username, max_age=30 * 24 * 60 * 60)
            return response
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form,
        'profile': profile,
        'login_count': request.session.get('login_count', 0),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def set_theme_view(request):
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        response = redirect('profile')
        response.set_cookie('theme', theme, max_age=365 * 24 * 60 * 60)
        messages.success(request, f'Theme set to {theme}.')
        return response
    return redirect('profile')
