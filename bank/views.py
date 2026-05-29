from django.shortcuts import render, redirect
from django.db.models import Sum

from .forms import (
    BankAccountForm,
    DepositForm,
    WithdrawalForm
)

from .models import (
    BankAccount,
    BankTransaction
)


# ==============================
# BANK ACCOUNT LIST
# ==============================

def bank_list(request):

    accounts = BankAccount.objects.all()

    context = {
        'accounts': accounts
    }

    return render(
        request,
        'bank_list.html',
        context
    )


# ==============================
# ADD BANK ACCOUNT
# ==============================

def add_bank_account(request):

    form = BankAccountForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect('bank_list')

    context = {
        'form': form
    }

    return render(
        request,
        'add_bank_account.html',
        context
    )


# ==============================
# ADD DEPOSIT
# ==============================

def add_deposit(request):

    form = DepositForm(
        request.POST or None
    )

    if form.is_valid():

        deposit = form.save(commit=False)

        deposit.transaction_type = 'DEPOSIT'

        deposit.save()

        return redirect('bank_list')

    context = {
        'form': form
    }

    return render(
        request,
        'add_deposit.html',
        context
    )


# ==============================
# ADD WITHDRAWAL
# ==============================

def add_withdrawal(request):

    form = WithdrawalForm(
        request.POST or None
    )

    if form.is_valid():

        withdrawal = form.save(commit=False)

        withdrawal.transaction_type = 'WITHDRAWAL'

        withdrawal.save()

        return redirect('bank_list')

    context = {
        'form': form
    }

    return render(
        request,
        'add_withdrawal.html',
        context
    )


# ==============================
# BANK REPORTS
# ==============================

# def bank_reports(request):

#     transactions = BankTransaction.objects.all()

#     context = {
#         'transactions': transactions
#     }

#     return render(
#         request,
#         'bank_reports.html',
#         context
#     )



# BANK REPORTS VIEW
# ==============================
# BANK REPORTS
# ==============================

def bank_reports(request):

    transactions = BankTransaction.objects.all().order_by('-date')

    # ------------------------------
    # FILTERS
    # ------------------------------

    report_type = request.GET.get('report_type')
    account_id = request.GET.get('account')
    transaction_type = request.GET.get('transaction_type')

    if account_id:

        transactions = transactions.filter(
            bank_account_id=account_id
        )

    if transaction_type:

        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    # ------------------------------
    # SUMMARY
    # ------------------------------

    total_deposits = transactions.filter(
        transaction_type='DEPOSIT'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_withdrawals = transactions.filter(
        transaction_type='WITHDRAWAL'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    current_balance = total_deposits - total_withdrawals

    # ------------------------------
    # ACCOUNTS
    # ------------------------------

    accounts = BankAccount.objects.all()

    context = {

        'transactions': transactions,

        'accounts': accounts,

        'total_deposits': total_deposits,

        'total_withdrawals': total_withdrawals,

        'current_balance': current_balance,

        'total_records': transactions.count(),

        'selected_account': account_id,

        'selected_transaction_type': transaction_type,

        'selected_report_type': report_type,

    }

    return render(
        request,
        'bank_reports.html',
        context
    )