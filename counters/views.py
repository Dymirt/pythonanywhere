from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic import CreateView
from counters.forms import ReadingForm, CounterForm

from counters.models import Counter, Reading


class CounterListView(ListView):
    model = Counter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ReadingListView(ListView):
    model = Reading
    template_name = "counters/reading_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(counter__user=self.request.user)
        return queryset


class CounterDetailView(DetailView):
    model = Counter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class AddCounterReading(CreateView):
    template_name = "counters/generic_update.html"
    form_class = ReadingForm
    success_url = reverse_lazy("counters:readings-list")

    def form_valid(self, form):
        if form.is_valid():
            if form.cleaned_data['counter'] in self.request.user.counters.all():
                return super().form_valid(form)
            else:
                form.add_error('counter', 'This is not your counter')  # Add a custom error message to the 'user' field

        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user object to the form
        return kwargs


class AddCounter(LoginRequiredMixin, CreateView):
    form_class = CounterForm
    template_name = "counters/generic_update.html"
    success_url = reverse_lazy("counters:counters-list")

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            return super().form_valid(form)
        return self.form_invalid(form)


class SummaryView(ListView):
    model = Counter
    template_name = "counters/summary.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class CounterUpdateView(UpdateView):
    form_class = CounterForm
    success_url = reverse_lazy("counters:readings-list")
    template_name = "counters/generic_update.html"

    def get_queryset(self):
        return Counter.objects.filter(user=self.request.user)


class ReadingUpdateView(UpdateView):
    form_class = ReadingForm
    success_url = reverse_lazy("counters:readings-list")
    template_name = "counters/generic_update.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('counter')  # Remove the 'counter' field from the form
        return form

    def get_queryset(self):
        return Reading.objects.filter(counter__user=self.request.user)


