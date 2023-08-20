from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from . import views
from django.http import HttpResponse
from .models import LibraryEntity
from .models import Authorize, Book, Assigned_material
from .forms import AuthorizeForm

#auth = [
#    {'id':1, 'name': 'Исходная библиотека - регистрация'},
#    {'id':2, 'name': 'Корневой каталог - доступ (чтение)'},
#    {'id':3, 'name': 'Корневой каталог - доступ (запись)'}
#]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Homepage')
    if request.method == 'POST':
        username = request.POST.get('Логин пользователя').lower()
        password = request.POST.get('Пароль')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Такого пользователя не существует')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Homepage')
        else:
            messages.error(request, 'Такой пары пользователь/пароль не существует')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('Homepage')

def registerUser(request):
    #page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Homepage')
        else:
            messages.error(request, 'Возникла ошибка при регистрации')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)
def home(request):
    # render different context in different cases
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    Auth = Authorize.objects.filter(
        Q(assigned__library_entity_id__book__name__icontains=q) |
        Q(name__contains=q) |
        Q(assigned__library_entity_id__description__contains=q)
    )
    #__icontains - case insensitive parameter.
    books = Book.objects.all()
    authorize_count = Auth.count()
    #.len() mathod also available
    context = {'authorize_mode': Auth, 'books': books, 'Authorize_count': authorize_count}
    return render(request, 'base/home.html', context)

def authorize(request, pk):
    Auth_id = Authorize.objects.get(id=pk)
    comments = Auth_id.assigned_material_set.all().order_by('-created')  # query child objects of a Auth-id
    if request.method == "POST":
        comment = Assigned_material.objects.create(
            user_id=request.user,
            authorize_id=Auth_id,
            body=request.POST.get('body')
        )
        return redirect('Authorize', pk=Auth_id.id)

    context = {'auth_id': Auth_id, 'comments': comments}
    return render(request, 'base/authorize.html', context)

def navbar(request):
    return render(request, 'navbar.html')

@login_required(login_url='login') # type of user check!
def create_resource(request):
    #read about requests
    form = AuthorizeForm()
    if request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Homepage')
    context = {'form': form}
    return render(request, 'base/authorize_form.html', context)

@login_required(login_url='login')
def update_resource(request, pk):
    auth = Authorize.objects.get(id=pk)
    form = AuthorizeForm(instance=auth)
    if request.user != auth.host or auth.mode <= 0:
        return HttpResponse('Этот раздел сайта доступен только пользователю ' + str(auth.host))
    if request.method =='POST':
        form = AuthorizeForm(request.POST,instance=auth)
        if form.is_valid():
            form.save()
            return redirect('Homepage')
    context = {'form':form}
    return render(request, 'base/authorize_form.html', context)
@login_required(login_url='login')
def delete_resource(request, pk):
    auth = Authorize.objects.get(id=pk)
    if request.method == 'POST':
        auth.delete()
        return redirect('Homepage')
    return render(request, 'base/delete.html', {'obj':auth})