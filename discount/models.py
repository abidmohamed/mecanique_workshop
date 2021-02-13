from django.db import models

# Create your models here.
from sellorder.models import Order


class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = (
        ('Percentage', 'Percentage'),
        ('Amount', 'Amount'),
    )
    discount_status = models.CharField(max_length=10, choices=discount_type, blank=True, default="Percentage")
