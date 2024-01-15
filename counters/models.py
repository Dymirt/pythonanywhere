from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


class Counter(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="counters"
    )
    title = models.CharField(max_length=60)
    unit = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def current_price(self):
        return self.prices.filter(date__lte=datetime.date(datetime.now())).last()


class Reading(models.Model):
    class Meta:
        ordering = ("-date",)

    counter = models.ForeignKey(
        "Counter", related_name="readings", on_delete=models.CASCADE
    )
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.counter.title} {self.value} on {self.date}"

    def get_previous_reading(self):
        return self.counter.readings.filter(pk__lt=self.pk).order_by("-pk").first()

    def usage_in_units(self):
        previous_reading = self.get_previous_reading()
        if previous_reading:
            return float(self.value) - float(previous_reading.value)
        else:
            return 0


class Price(models.Model):
    class Meta:
        ordering = ("date",)

    counter = models.ForeignKey(
        "Counter", related_name="prices", on_delete=models.CASCADE
    )
    date = models.DateField()
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    price_per_month = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.price_per_unit}/{self.counter.unit} and {self.price_per_month}/month" if self.price_per_month else f"{self.price_per_unit}/{self.counter.unit}"


class Payment(models.Model):
    counter = models.ForeignKey(
        "Counter", related_name="payments", on_delete=models.CASCADE
    )
    reading = models.OneToOneField(
        "Reading", related_name="payment", on_delete=models.CASCADE
    )
    price = models.ForeignKey(
        "Price", related_name="payments", on_delete=models.CASCADE
    )

    def reading_payment(self):
        if self.reading.get_previous_reading():
            if self.reading.usage_in_units():
                total = self.reading.usage_in_units() * float(
                    self.reading.counter.prices.filter(date__lte=self.reading.date).last().price_per_unit
                )
                return round(
                    total + float(self.reading.counter.prices.filter(date__lte=self.reading.date).last().price_per_month)
                    if self.reading.counter.prices.filter(date__lte=self.reading.date).last().price_per_month
                    else total, 2)
            return self.reading.counter.prices.filter(date__lte=self.reading.date).last().price_per_month
