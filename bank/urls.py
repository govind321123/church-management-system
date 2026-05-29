from django.urls import path
from . import views


urlpatterns = [

    # Bank List
    path(
        '',
        views.bank_list,
        name='bank_list'
    ),

    # Add Bank Account
    path(
        'add/',
        views.add_bank_account,
        name='add_bank_account'
    ),

    # Deposit Entry
    path(
        'deposit/add/',
        views.add_deposit,
        name='add_deposit'
    ),

    # Withdrawal Entry
    path(
        'withdrawal/add/',
        views.add_withdrawal,
        name='add_withdrawal'
    ),

    # Bank Reports
    path(
        'reports/',
        views.bank_reports,
        name='bank_reports'
    ),

]