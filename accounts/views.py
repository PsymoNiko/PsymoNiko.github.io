from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import generics

from .forms import CustomUserRegistrationForm
from .models import User
from .serialiezrs import UserSerializer


class CreateUserViews(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('index')  # Redirect to the home page after successful registration
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.phone_number}!')
            return redirect('index')  # Redirect to the home page after successful registration
        else:
            messages.error(request, 'Invalid registration details. Please check the form.')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to your login page
