from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    file_url = models.URLField()
    date_published = models.DateField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField()
    cover_image = models.URLField()
    genres = models.ManyToManyField(Genre, related_name="books")  # many-to-many
    description = models.TextField(blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    books = models.ManyToManyField('Book', related_name='users', blank=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )

    def __str__(self):
        return self.username