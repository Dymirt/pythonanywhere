import django.forms
from django.forms import ModelForm, DateInput, widgets
from .models import Book
import django_filters.widgets
from datetime import datetime


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            "published_date": DateInput(attrs={
                'type': 'date',
                'max': datetime.now().date().strftime('%Y-%m-%d')
            })
        }