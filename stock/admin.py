from django.contrib import admin

# Register your models here.
from stock.models import StockProduct


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ['product',]
