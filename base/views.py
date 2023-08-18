from django.shortcuts import render, redirect
from . import views
from django.http import HttpResponse
from .models import LibraryEntity
from .models import Authorize
from .forms import AuthorizeForm

#auth = [
#    {'id':1, 'name': 'Исходная библиотека - регистрация'},
#    {'id':2, 'name': 'Корневой каталог - доступ (чтение)'},
#    {'id':3, 'name': 'Корневой каталог - доступ (запись)'}
#]

def home(request):
    # render different context in different cases
    Auth = Authorize.objects.all()
    context = {'authorize_mode': Auth}
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
    context = {'form':form}
    return render(request, 'base/authorize_form.html', context)