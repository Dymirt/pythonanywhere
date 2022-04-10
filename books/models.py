from django.db import models
from isbn_field import ISBNField

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100, blank=False)
    published_date = models.DateField(blank=False)
    isbn = ISBNField()
    page_count = models.IntegerField(blank=False)
    imageLinks = models.URLField()
    language = models.CharField(max_length=2)

    def __str__(self):
        return self.title
