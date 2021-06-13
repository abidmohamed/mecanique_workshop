from django.contrib import admin

# Register your models here.
from customer.models import Customer, Enterprise


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'phone', 'debt')


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'rc', 'nif', 'nis', 'art')