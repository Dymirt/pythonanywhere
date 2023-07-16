from django.urls import path, reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from counters.models import Counter, Reading
from django.contrib.auth.decorators import login_required

from counters.views import (
    CounterListView,
    ReadingListView,
    CounterDetailView,
    update_usage,
    SummaryView,
    AddCounterReading,
)

app_name = "counters"

urlpatterns = [
    #path("counters/", SummaryView.as_view(), name="dashboard"),
    path("counters/summary", SummaryView.as_view(), name="summary"),
    # Counters urls
    path("counters/list/", CounterListView.as_view(), name="counters-list"),
    path(
        "counter/create/",
        login_required(
            CreateView.as_view(
                model=Counter,
                fields="__all__",
                success_url=reverse_lazy("counters:counters-list"),
                template_name="counters/generic_update.html",
            )
        ),
        name="counter-create",
    ),
    path(
        "counter/<int:pk>/edit/",
        UpdateView.as_view(
            model=Counter,
            fields="__all__",
            success_url=reverse_lazy("counters:counters-list"),
            template_name="counters/generic_update.html",
        ),
        name="counter-edit",
    ),
    path(
        "counter/<int:pk>/delete/",
        login_required(
            DeleteView.as_view(
                model=Counter,
                success_url=reverse_lazy("counters:counters-list"),
                template_name="counters/generic_delete.html",
            )
        ),
        name="counter-delete",
    ),
    path("counter/<int:pk>/detail/", CounterDetailView.as_view(), name="counter-detail"),
    # Reading urls
    path("readings/list/", ReadingListView.as_view(), name="readings-list"),
    path("reading/create/", AddCounterReading.as_view(), name="reading-create"),
    path(
        "reading/<int:pk>/edit/",
        UpdateView.as_view(
            model=Reading,
            fields="__all__",
            success_url=reverse_lazy("counters:readings-list"),
            template_name="counters/generic_update.html",
        ),
        name="reading-edit",
    ),
    path(
        "reading/<int:pk>/delete/",
        login_required(
            DeleteView.as_view(
                model=Reading,
                success_url=reverse_lazy("counters:readings-list"),
                template_name="counters/generic_delete.html",
            )
        ),
        name="reading-delete",
    ),
]
