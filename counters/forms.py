from django.forms import ModelForm
from django.forms.widgets import DateInput
from .models import Reading


class ReadingForm(ModelForm):
    class Meta:
        model = Reading
        fields = ('counter', 'date', 'value')

        widgets = {
            'date': DateInput(attrs={"type": "date"}),
        }
