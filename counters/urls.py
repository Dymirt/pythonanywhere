from django.urls import path, reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from .models import Counter, Reading

from .views import CounterListView, ReadingListView

app_name = 'counters'

urlpatterns = [
    # Counters urls
    path('counters/list/', CounterListView.as_view(), name='counters-list'),
    path('counter/create/',
         CreateView.as_view(
             model=Counter,
             fields='__all__',
             success_url=reverse_lazy('counters:counters-list'),
             template_name='counters/generic_update.html'
         ),
         name='counter-create'),
    path('counter/<int:pk>/edit/',
         UpdateView.as_view(
             model=Counter,
             fields='__all__',
             success_url=reverse_lazy('counters:counters-list'),
             template_name='counters/generic_update.html'
         ),
         name='counter-edit'),
    path('counter/<int:pk>/delete/',
         DeleteView.as_view(
             model=Counter,
             success_url=reverse_lazy('counters:counters-list'),
             template_name='counters/generic_delete.html'
         ),
         name='counter-delete'),
    # Reading urls
    path('readings/list/', ReadingListView.as_view(), name='readings-list'),
    path('reading/create/',
         CreateView.as_view(
             model=Reading,
             fields='__all__',
             success_url=reverse_lazy('counters:readings-list'),
             template_name='counters/generic_update.html'
         ),
         name='reading-create'),
    path('reading/<int:pk>/edit/',
         UpdateView.as_view(
             model=Reading,
             fields='__all__',
             success_url=reverse_lazy('counters:readings-list'),
             template_name='counters/generic_update.html'
         ),
         name='reading-edit'),
    path('reading/<int:pk>/delete/',
         DeleteView.as_view(
             model=Reading,
             success_url=reverse_lazy('counters:readings-list'),
             template_name='counters/generic_delete.html'
         ),
         name='reading-delete'),
]
