from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Authorize, Book, Assigned_material, LibraryEntity
from .forms import AuthorizeForm, UserForm, fileForm
from django.core.files.storage import FileSystemStorage

#auth_id = [
#    {'id':1, 'name': 'Исходная библиотека - регистрация'},
#    {'id':2, 'name': 'Корневой каталог - доступ (чтение)'},
#    {'id':3, 'name': 'Корневой каталог - доступ (запись)'}
#]


def loginPage(request):
    page = 'login'
    if request.user.is_auth_identicated:
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
    auth_id = Authorize.objects.filter(
        Q(assigned__library_entity_id__book__name__icontains=q) |
        Q(name__contains=q) |
        Q(assigned__library_entity_id__description__contains=q)
    )
    books = Book.objects.all()[0:5]
    Authorize_count = auth_id.count()
    auth_comments = Assigned_material.objects.filter(Q(library_entity_id__book__name__icontains=q))
    assigned_count = auth_comments.count()
    context = {'authorize_mode': auth_id, 'books': books, 'Authorize_count': Authorize_count, 'auth_comments': auth_comments, 'assigned_count': assigned_count}
    return render(request, 'base/home.html', context)


def authorize(request, pk):
    auth_id = Authorize.objects.get(id=pk)
    comments = auth_id.assigned_material_set.all()
    participants = auth_id.participants.all()
    if request.method == "POST":
        comment = Assigned_material.objects.create(
            user_id=request.user,
            Authorize_id=auth_id,
            body=request.POST.get('body')
        )
        auth_id.participants.add(request.user)
        return redirect('Authorize', pk=auth_id.id)

    context = {'auth_id_id': auth_id, 'comments': comments, 'participants': participants}
    return render(request, 'base/authorize.html', context)


def navbar(request):
    return render(request, 'navbar.html')


def userProfile(request, pk):
    user_opened = User.objects.get(id=pk)
    Authorize_mode = user_opened.Authorize_set.all()
    auth_id_comments = user_opened.assigned_material_set.all()
    books = Book.objects.all()
    context = {'user': user_opened, 'authorize_mode': Authorize_mode, 'auth_id_comments': auth_id_comments, 'books': books}
    return render(request,'base/profile.html', context)


@login_required(login_url='login') # type of user check!
def create_resource(request):
    form = AuthorizeForm()
    books = Book.objects.all()
    if request.method == 'POST':
        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(name=book_name)
        Authorize.objects.create(
            host=request.user,
            book=book,
            name=request.POST.get('name'),
            mode=0,
            login=User.username,
            password=User.username,  # cannot retrieve password directly
            description=request.POST.get('description')
        )
        return redirect('Homepage')
    context = {'form': form, 'books': books}
    return render(request, 'base/authorize_form.html', context)


@login_required(login_url='login')
def update_resource(request, pk):
    auth_id = Authorize.objects.get(id=pk)
    form = AuthorizeForm(instance=auth_id)
    books = Book.objects.all()
    if request.user != auth_id.host: # or auth_id.mode <= 0:
        return HttpResponse('Этот раздел сайта доступен только пользователю ' + str(auth_id.host))
    if request.method == 'POST':
        book_name = request.POST.get('book')
        book, created = Book.objects.get_or_create(name=book_name)
        auth_id.name = request.POST.get('name')
        auth_id.book = book
        auth_id.description = request.POST.get('description')
        auth_id.save()
        return redirect('Homepage')
    context = {'form': form, 'books': books, 'auth_id': auth_id}
    return render(request, 'base/authorize_form.html', context)


@login_required(login_url='login')
def delete_resource(request, pk):
    auth_id = Authorize.objects.get(id=pk)
    if request.method == 'POST':
        auth_id.delete()
        return redirect('Homepage')
    context = {'obj': auth_id}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_comment(request, pk):
    auth_id_m = Assigned_material.objects.get(id=pk)
    if request.user != auth_id_m.user_id:
        return HttpResponse('Для данного действия не хватает полномочий')
    if request.method == 'POST':
        auth_id_m.delete()
        return redirect('Homepage') # ('Authorize', pk=auth_id_id.id)
    context = {'obj': auth_id_m}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update_profile.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Book.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activitiesPage(request):
    auth_id_comments = Assigned_material.objects.all()
    return render(request, 'base/activity.html', {'auth_id_comments': auth_id_comments})

def file_upload(request):
    if request.method == 'POST':
        form_file = fileForm(request.POST, request.FILES)
        if form_file.is_valid():
            form_file.save()
            return HttpResponse('The file is saved')
    else:
        form_file = fileForm()
        context = {
            'form_file': form_file,
        }
    return render(request, 'base/file_upload.html', context)