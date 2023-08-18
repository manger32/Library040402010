from django.forms import ModelForm
from .models import Authorize

class AuthorizeForm(ModelForm):
    class Meta:
        model = Authorize
        fields = '__all__' # ['name', 'body']