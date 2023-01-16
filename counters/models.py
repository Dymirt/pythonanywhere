from django.db import models

# Create your models here.


class Counter(models.Model):
    title = models.CharField(max_length=60)
    consumable = models.BooleanField(default=True)
    unit = models.CharField(max_length=60, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fixed_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class Reading(models.Model):
    class Meta:
        ordering = ('-date',)

    counter = models.ForeignKey('Counter', related_name='readings', on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    usage_in_units = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.counter.title} {self.value} on {self.date}'
