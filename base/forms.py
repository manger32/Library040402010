from django.forms import ModelForm
from .models import Authorize
from django.contrib.auth.models import User

class AuthorizeForm(ModelForm):
    class Meta:
        model = Authorize
        fields = '__all__' # ['name', 'body']
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']