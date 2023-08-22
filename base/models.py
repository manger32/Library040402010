from django.db import models
from django.contrib.auth.models import User
# Database model and Admin panel

class Authorize(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    class Mode(models.IntegerChoices):
        admin = 0
        test = -1
        user = 1
        librarian = 2
        guest = 3
    name = models.CharField(max_length=50)
    mode = models.IntegerField(choices = Mode.choices)
    login = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    assigned = models.ForeignKey('Assigned_material', on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated', '-created'] #without dashes ascending order
    def __str__(self):
        return self.name
class Book(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class LibraryEntity(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    access_rights = models.ForeignKey(Authorize, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    year = models.IntegerField()
    publication = models.CharField(max_length = 20)
    abstract = models.TextField(null = True, blank = True)
    #authors =
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    # uuid = # by default, ids are generated from the dictionary of Authorize ids

    def __str__(self):
        return str( self.name)

class Assigned_material(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    authorize_id = models.ForeignKey(Authorize, on_delete=models.CASCADE)
    library_entity_id = models.ForeignKey(LibraryEntity, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length = 90)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.body[0:40]
# Create your models here.
