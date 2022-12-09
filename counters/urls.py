from django.urls import path, reverse_lazy
from django.views.generic import UpdateView, CreateView,  DeleteView
from .models import Counter

from .views import CounterListView

app_name = 'counters'


urlpatterns = [

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
]