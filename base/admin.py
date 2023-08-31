from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Authorize)
admin.site.register(Book)
admin.site.register(LibraryEntity)
admin.site.register(Assigned_material)