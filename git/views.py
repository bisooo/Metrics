from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from git.forms import RegistrationForm, LoginForm
# GITHUB LIBRARY


def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=password)
            auth_login(request, account)
            return redirect('homepage')
        else:
            context['register_form'] = form
    else:
        form = RegistrationForm()
        context['register_form'] = form

    return render(request, 'register.html', context)


def login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('homepage')
    else:
        form = LoginForm()
    context['login_form'] = form

    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')
