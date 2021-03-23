from django.contrib import admin

# Register your models here.
from sellorder.models import Order, SellOrderFacture


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created')


@admin.register(SellOrderFacture)
class BillOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'created')
