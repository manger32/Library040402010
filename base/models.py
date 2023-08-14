from django.db import models

# Database model and Admin panel

class Authorize(models.Model):
    #host =
    class Mode(models.IntegerChoices):
        admin = 0
        test = -1
        user = 1
        librarian = 2

    mode = models.IntegerField(choices = Mode.choices)
    login = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)

class LibraryEntity(models.Model):
    #host =
    #access_rights = #0 - admin; -1 - test; 1 - user; 2 - librarian
    description = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    year = models.IntegerField()
    publication = models.CharField(max_length = 20)
    abstract = models.TextField(null = True, blank = True)
    #authors =
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return str( self.name)

#class Worker
# Create your models here.
