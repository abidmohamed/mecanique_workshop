from django.contrib import admin

# Register your models here.
from sellorder.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created')
