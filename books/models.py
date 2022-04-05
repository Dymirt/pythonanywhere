from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, related_name="authored")
    published_date = models.DateField()
    isbn = models.CharField(max_length=50)
    page_count = models.IntegerField()
    imageLinks = models.URLField()
    language = models.CharField(max_length=2)



