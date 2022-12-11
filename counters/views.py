from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import Counter, Reading
from .reports import summary_per_month


class CounterListView(ListView):
    model = Counter


class ReadingListView(ListView):
    model = Reading


class CounterDetailView(DetailView):
    model = Counter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summary'] = summary_per_month(self.object.readings.all())
        return context


def update_usage(request):
    counters = Counter.objects.all().filter(consumable=True)
    for counter in counters:
        readings = counter.readings.all()[:2]
        latest = readings[0]
        previous = readings[1]
        latest.usage_in_units = latest.value - previous.value
        latest.save(update_fields=['usage_in_units'])


class IndexView(ListView):
    model = Counter
    template_name = 'counters/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summary_per_month'] = {obj: summary_per_month(obj.readings.all()) for obj in self.object_list}
        context['total'] = sum([context['summary_per_month'].get(i)[0][2] for i in context['summary_per_month']])
        return context
