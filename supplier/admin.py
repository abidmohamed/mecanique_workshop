from django.contrib import admin

# Register your models here.
from supplier.models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'phone', 'email', 'credit')