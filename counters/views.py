from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic import CreateView
from counters.forms import ReadingForm

from .models import Counter, Reading


class CounterListView(ListView):
    model = Counter


class ReadingListView(ListView):
    model = Reading
    template_name = "counters/reading_list.html"


class CounterDetailView(DetailView):
    model = Counter


class AddCounterReading(CreateView):
    template_name = "counters/generic_update.html"
    form_class = ReadingForm
    success_url = reverse_lazy("counters:readings-list")


def update_usage(request):
    counters = Counter.objects.all().filter(consumable=True)
    for counter in counters:
        readings = counter.readings.all()[:2]
        latest = readings[0]
        previous = readings[1]
        latest.usage_in_units = latest.value - previous.value
        latest.save(update_fields=["usage_in_units"])


class SummaryView(ListView):
    model = Counter
    template_name = "counters/summary.html"

