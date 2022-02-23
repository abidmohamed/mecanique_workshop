from django.contrib import admin

# Register your models here.
from buyorder.models import BuyOrder


@admin.register(BuyOrder)
class BuyorderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'created')
    search_fields = ['id', ]
