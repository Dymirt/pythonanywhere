import django_filters
from django_filters.widgets import RangeWidget

from .models import Book
from django.db import models


class BookFilter(django_filters.FilterSet):
    published_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'author': ['contains'],
            'language': ['contains']
        }