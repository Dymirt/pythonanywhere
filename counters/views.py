import calendar
from datetime import datetime

from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, View, CreateView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.contrib.auth import get_user_model

from django.db.models.functions import ExtractMonth, ExtractYear

from .forms import (
    AddCounterForm,
    AddCounterPriceForm,
    AddCounterReadingForm,
    UpdateCounterForm,
)
from .models import Counter, Reading, Price, Payment

from django.db.models import OuterRef, Subquery, Max, F, ExpressionWrapper, DecimalField, Sum


def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("counters:dashboard"))
    else:
        return render(request, "counters/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("counters:dashboard"))
        else:
            return render(
                request,
                "counters/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "counters/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("counters:login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        if not username:
            return render(
                request, "counters/register.html", {"message": "Username is required"}
            )

        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if len(password) < 8:
            return render(
                request,
                "counters/register.html",
                {"message": "Passwords must contain at least 8 characters."},
            )

        if password != confirmation:
            return render(
                request, "counters/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = get_user_model().objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "counters/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("counters:dashboard"))
    else:
        return render(request, "counters/register.html")


class CounterDetailView(DetailView):
    model = Counter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counter = context["object"]
        # Calculate usage dynamically in the view
        # Calculate usage dynamically in the view
        readings = (
            Reading.objects.filter(counter=counter)
            .annotate(
                month=ExtractMonth("date"),
                previous_value=Subquery(
                    Reading.objects.filter(
                        counter=OuterRef("counter"),
                        date__lt=OuterRef("date"),
                    )
                    .order_by("-date")
                    .values("value")[:1]
                ),
            )
            .values("month", "value", "previous_value")
            .order_by("date")
        )

        # Calculate usage based on value and previous_value
        readings_usage = [
            float(reading["value"] - reading["previous_value"])
            if reading["previous_value"] is not None
            else 0
            for reading in readings
        ]

        readings_month = [
            calendar.month_name[reading.get("month")] for reading in readings
        ]
        #readings_usage = [float(reading.get("usage")) for reading in readings]

        context["readings_month"] = readings_month
        context["readings_usage"] = readings_usage
        return context


class AddCounter(LoginRequiredMixin, CreateView):
    form_class = AddCounterForm
    template_name = "counters/generic_update.html"
    success_url = reverse_lazy("counters:dashboard")

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            response = super().form_valid(form)

            # Get the counter by its name
            counter_name = form.cleaned_data["title"]
            try:
                counter = Counter.objects.get(
                    user=self.request.user, title=counter_name
                )
            except Counter.DoesNotExist:
                # Handle the case when the counter with the given name doesn't exist
                # (e.g., show an error message or redirect to an error page)
                raise ValueError("Counter with the given name does not exist.")

            # Validate the AddCounterPriceForm
            price_form = AddCounterPriceForm(self.request.POST)
            if price_form.is_valid():
                Price.objects.create(
                    counter=counter,
                    date=form.cleaned_data["initial_date"],
                    price_per_unit=price_form.cleaned_data["price_per_unit"],
                    price_per_month=price_form.cleaned_data["price_per_month"],
                )

            # Validate the AddCounterReadingForm
            reading_form = AddCounterReadingForm(self.request.POST)
            if reading_form.is_valid():
                Reading.objects.create(
                    counter=counter,
                    date=form.cleaned_data["initial_date"],
                    value=reading_form.cleaned_data["value"],
                )

            return response
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "price_form"
        ] = AddCounterPriceForm()  # Include the CounterPriceForm in the context
        context["reading_form"] = AddCounterReadingForm()
        return context


class SummaryView(ListView):
    model = Counter
    template_name = "counters/summary.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_reading_date = latest_reading_date_for_user_counters(self.request.user)
        if latest_reading_date:
            context["latest_reading_date"] = latest_reading_date.strftime("%Y-%m-%d")
        context["counter_form"] = AddCounterForm()

        context["payments_per_month"] = (
            Reading.objects.filter(counter__user=self.request.user)
            .annotate(
                month=ExtractMonth("date"),
                year=ExtractYear("date"),
                previous_value=Subquery(
                    Reading.objects.filter(
                        date__lt=OuterRef("date"),
                        counter=OuterRef("counter"),
                    ).order_by("-date").values("value")[:1]
                ),
                usage_in_units=ExpressionWrapper(
                    F("value") - F("previous_value"),
                    output_field=DecimalField(),
                ),
                price_per_unit=Subquery(
                    Price.objects.filter(
                        counter=OuterRef("counter"),
                        date__lte=OuterRef("date"),
                    ).order_by("-date").values("price_per_unit")[:1]
                ),
                price_per_month=Subquery(
                    Price.objects.filter(
                        counter=OuterRef("counter"),
                        date__lte=OuterRef("date"),
                    ).order_by("-date").values("price_per_month")[:1]
                ),
            )
            .values("month", "year")
            .annotate(
                total_payment=Sum(
                    ExpressionWrapper(
                        F("usage_in_units") * F("price_per_unit") + F("price_per_month"),
                        output_field=DecimalField(),
                    )
                )
            )
            .order_by("-year", "-month")
        )
        return context


def latest_reading_date_for_user_counters(user):
    return Reading.objects.filter(counter__user=user).aggregate(
        latest_date=Max("date")
    )["latest_date"]


def add_readings(request):
    if request.method == "POST":
        readings_date = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
        for counter in request.user.counters.all():
            # Only one reading per month if this not initial reading
            if counter.readings.exists() and counter.readings.count() > 1:
                latest_reading = counter.readings.latest("pk")

                # Return HttpResponseBadRequest if value of previous reading i greater than new value
                if float(latest_reading.value) > float(request.POST.get(counter.title)):
                    return HttpResponseBadRequest()

                # Delete the latest reading if reading in same month
                if latest_reading.date.month == readings_date.month:
                    latest_reading.delete()

            Reading.objects.create(
                counter=counter,
                date=readings_date,
                value=request.POST.get(counter.title),
            )

            latest_reading = counter.readings.latest("pk")

            # Adding Payment
            Payment.objects.create(
                counter=counter,
                reading=latest_reading,
                price=counter.prices.filter(date__lte=latest_reading.date).last(),
            )

        return redirect(reverse_lazy("counters:dashboard"))


class CounterUpdateView(UpdateView):
    form_class = UpdateCounterForm
    template_name = "counters/generic_update.html"

    def get_queryset(self):
        return Counter.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("counters:counter-detail", kwargs={"pk": self.object.pk})
