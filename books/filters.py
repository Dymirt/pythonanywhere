import django_filters
from django_filters.widgets import RangeWidget
from .models import Book


class BookFilter(django_filters.FilterSet):
    published_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date',
                                                                                    'class': 'date_range'
                                                                                    }))

    class Meta:
        model = Book
        fields = {
            'title': ['contains'],
            'author': ['contains'],
            'language': ['exact']
        }