from django.shortcuts import render
from . import views
from django.http import HttpResponse

auth = [
    {'id':1, 'name': 'Исходная библиотека - регистрация'},
    {'id':2, 'name': 'Корневой каталог - доступ (чтение)'},
    {'id':3, 'name': 'Корневой каталог - доступ (запись)'}
]

def home(request):
    # render different context in different cases
    context = {'authorize_mode':auth}
    return render(request, 'base/home.html', context)

def authorize(request, pk):
    auth_id = None
    for i in auth:
        if i['id'] == int(pk):
            auth_id = i
    context = {'auth_id':auth_id}
    return render(request, 'base/authorize.html', context)

def navbar(request):
    return render(request, 'navbar.html')