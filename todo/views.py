from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        #create new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                #above only returns user, does not save in Database
                user.save()
                #function to login user
                login(request, user)
                #A page to route them
                return redirect('currentTodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'User already exists'})
        else:
            # print('Passwords dont match')
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords do not match'})
            #passwords didnt match


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        #create new user
        # if request.POST['password1'] == request.POST['password2']:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        #A page to route them
        if user == None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'User does not exist'})
        else:
            login(request, user)
                #A page to route them
            return redirect('currentTodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currentTodos(request):
    return render(request, 'todo/currenttodos.html', {'form': UserCreationForm()})
