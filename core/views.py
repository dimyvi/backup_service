from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')