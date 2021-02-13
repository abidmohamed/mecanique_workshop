from django.contrib import admin

# Register your models here.
from caisse.models import Caisse, CaisseHistory, Transaction


@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    list_display = ('caisse_value',)


@admin.register(CaisseHistory)
class CaisseHistoryAdmin(admin.ModelAdmin):
    list_display = ('caisse_value', 'date_created')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('Transaction_name', 'amount', 'Transaction_type', 'trans_date')
