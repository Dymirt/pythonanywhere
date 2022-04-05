from django.shortcuts import render
from .filters import BookFilter
from django.views.generic import ListView
from .models import Book

# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = "books/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET,  queryset=self.get_queryset())
        return context
