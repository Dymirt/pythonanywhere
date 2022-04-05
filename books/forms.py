from django.forms import ModelForm
from .models import Book


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'page_count', 'imageLinks', 'language']