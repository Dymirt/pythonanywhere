from django.db.models import Sum, F
from django.db.models.functions import TruncMonth


def summary_per_month(queryset):
    return (
        queryset.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(c=Sum("usage_in_units"))
        .annotate(
            s=(Sum("usage_in_units") * F("counter__price_per_unit"))
            + F("counter__fixed_price")
        )
        .values_list("month", "c", "s")
        .order_by("-month")
    )
