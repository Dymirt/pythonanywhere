from django.shortcuts import render
from .filters import BookFilter
from django.views.generic import ListView
from django_tables2 import SingleTableMixin
from .models import Book
from .tables import BookTable
from django_filters.views import FilterView

# Create your views here.


class BookListView(SingleTableMixin, FilterView):
    model = Book
    template_name = "books/index.html"
    table_class = BookTable
    filterset_class = BookFilter
