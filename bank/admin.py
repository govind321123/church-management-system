from django.contrib import admin
from .models import (
    BankAccount,
    BankTransaction
)


# ======================================
# BANK ACCOUNT ADMIN
# ======================================

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):

    list_display = (
        'account_name',
        'bank_name',
        'account_number',
        'ifsc_code',
        'opening_balance',
        'current_balance',
        'created_at'
    )

    search_fields = (
        'account_name',
        'bank_name',
        'account_number'
    )

    list_filter = (
        'bank_name',
        'created_at'
    )

    ordering = (
        '-created_at',
    )


# ======================================
# BANK TRANSACTION ADMIN
# ======================================

@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'bank_account',
        'transaction_type',
        'date',
        'amount',
        'source',
        'purpose',
        'created_at'
    )

    search_fields = (
        'bank_account__account_name',
        'purpose'
    )

    list_filter = (
        'transaction_type',
        'date',
        'source'
    )

    ordering = (
        '-date',
        '-id'
    )