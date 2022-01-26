from django.contrib import admin

# Register your models here.
from accounts.models import CurrentYear


@admin.register(CurrentYear)
class CurrentYearAdmin(admin.ModelAdmin):
    list_display = ('year', )