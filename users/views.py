from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import UserRole,Role

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request,'invalid username or password')

    else:
        form = LoginForm()

    return render(request,'users/login.html',{'form':form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request,'You have successfully logged out.')
    return redirect('login')