from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')