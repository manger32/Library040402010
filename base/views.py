from django.shortcuts import render, redirect
from django.db.models import Q
from . import views
from django.http import HttpResponse
from .models import LibraryEntity
from .models import Authorize, Book
from .forms import AuthorizeForm

#auth = [
#    {'id':1, 'name': 'Исходная библиотека - регистрация'},
#    {'id':2, 'name': 'Корневой каталог - доступ (чтение)'},
#    {'id':3, 'name': 'Корневой каталог - доступ (запись)'}
#]

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
    context = {'auth_id': Auth_id}
    return render(request, 'base/authorize.html', context)

def navbar(request):
    return render(request, 'navbar.html')

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

def update_resource(request, pk):
    auth = Authorize.objects.get(id=pk)
    form = AuthorizeForm(instance=auth)
    if request.method =='POST':
        form = AuthorizeForm(request.POST,instance=auth)
        if form.is_valid():
            form.save()
            return redirect('Homepage')
    context = {'form':form}
    return render(request, 'base/authorize_form.html', context)

def delete_resource(request, pk):
    auth = Authorize.objects.get(id=pk)
    if request.method == 'POST':
        auth.delete()
        return redirect('Homepage')
    return render(request, 'base/delete.html', {'obj':auth})