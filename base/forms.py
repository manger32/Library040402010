from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Authorize, fileHandler, User

class UserCreation_Custom(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class AuthorizeForm(ModelForm):
    class Meta:
        model = Authorize
        fields = '__all__' # ['name', 'body']
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class fileForm(ModelForm):
    class Meta:
        model = fileHandler
        fields = ['file']