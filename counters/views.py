from django.shortcuts import render
from .models import Counter, Reading

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class CounterListView(ListView):
    model = Counter


class ReadingListView(ListView):
    model = Reading


class CounterDetailView(DetailView):
    model = Counter