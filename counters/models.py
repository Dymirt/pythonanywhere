from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.


class Counter(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="counters")
    title = models.CharField(max_length=60)
    consumable = models.BooleanField(default=True)
    unit = models.CharField(max_length=60, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fixed_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.title}"


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

    def usage_in_units(self):
        previous_reading = self.counter.readings.filter(pk__lt=self.pk).order_by('-pk').first()
        if previous_reading:
            return self.value - previous_reading.value

    def payment(self):
        if self.usage_in_units():
            total = self.usage_in_units() * self.counter.price_per_unit
            return total if not self.counter.fixed_price else total + self.counter.fixed_price

