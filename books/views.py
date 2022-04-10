from django.shortcuts import render, redirect
from django.urls import reverse

from .filters import BookFilter
from django.views.generic import ListView, FormView
from django_tables2 import SingleTableMixin
from .models import Book
from .tables import BookTable
from .forms import BookForm
from django_filters.views import FilterView

# Create your views here.


class BookListView(SingleTableMixin, FilterView):
    model = Book
    template_name = "books/index.html"
    table_class = BookTable
    filterset_class = BookFilter


class BookAdd(FormView):
    form_class = BookForm
    template_name = "books/add_book.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            if not Book.objects.filter(title=form.cleaned_data['title']).exists():
                return self.form_valid(form)
        return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        form.save()
        return render(self.request, 'books/succes_add_book.html', context={'message': "Congratulations! Book was successfully added to list."})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        context['message'] = 'Book was NOT successfully added to list. Book already in list'
        return self.render_to_response(context)
