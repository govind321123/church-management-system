from django.contrib import admin
from .models import Expenditure


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'category',
        'amount',
        'approved_by',
        'payment_mode'
    )

    list_filter = ('category', 'payment_mode')
    search_fields = ('description', 'approved_by')
