from django.contrib import admin
from payments.models import SellOrderPayment, BuyOrderPayment


# Register your models here.
@admin.register(SellOrderPayment)
class SellOrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'amount', 'created', 'pay_status')


@admin.register(BuyOrderPayment)
class BuyOrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'supplier', 'amount', 'created', 'pay_status')
