from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib import messages

from .forms import *
from .models import *


def registration_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Пользователь " + user + " был успешно создан!")
            return redirect('login')

            
    context = {
		'form': form,
        'header': 'Регистрация',
	}
    return render(request, 'user_app/registration.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Логин или пароль введен неверно')

    context = {
        'header': 'Авторизация',
    }
    return render(request, 'user_app/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')
