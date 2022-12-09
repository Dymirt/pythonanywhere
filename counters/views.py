from django.shortcuts import render
from .models import Counter, Reading

# Create your views here.
from django.views.generic.list import ListView


class CounterListView(ListView):
    model = Counter


class ReadingListView(ListView):
    model = Reading
