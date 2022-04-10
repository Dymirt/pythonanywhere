import django_tables2 as tables
from django.utils.html import format_html
from .models import Book


class BookTable(tables.Table):
    image = tables.TemplateColumn('<img src="{{record.imageLinks}}" class="img-thumbnail">',
                                  orderable=False)

    class Meta:
        model = Book
        fields = ('title', 'author', 'published_date', 'isbn', 'page_count', 'language')
        attrs = {"class": "table table-hover"}


