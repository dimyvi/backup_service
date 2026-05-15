from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'users/register.html', {
                'error': 'Fill all fields'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {
                'error': 'User already exists'
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('/backups/dashboard/')

    return render(request, 'users/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/backups/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/backups/dashboard/')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')