from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, decorators

# Create your views here.
from .forms import TodoForm
from .models import Todo

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

@decorators.login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@decorators.login_required
def currentTodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todoList': todos})

@decorators.login_required
def createTodos(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html', {'form': TodoForm()})
    elif request.method == 'POST':
        form = TodoForm(request.POST)
        try:
            if form.is_valid():
                newForm = form.save(commit=False)
                # map the user where to save
                newForm.user = request.user
                newForm.save()
                return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/createTodo.html', {'form': TodoForm(), 'error': 'Bad data passed'})

@decorators.login_required
def viewTodo(request, todo_pk):

    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewAndEditTodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            if form.is_valid():
                form.save()
                return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/viewAndEditTodo.html', {'form': TodoForm(), 'error': 'Bad data passed'})


@decorators.login_required
def completeTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentTodos')

@decorators.login_required
def deleteTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentTodos')

@decorators.login_required
def completedTodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/currenttodos.html', {'todoList': todos, 'completed': True})