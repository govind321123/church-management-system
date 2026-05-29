from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils.timezone import now

from .models import Expenditure
from .forms import ExpenditureForm


# ==============================
# EXPENDITURE LIST
# ==============================

def expenditure_list(request):

    expenditures = Expenditure.objects.all().order_by('-date')

    context = {
        'expenditures': expenditures
    }

    return render(
        request,
        'expenditure_list.html',
        context
    )


# ==============================
# ADD EXPENDITURE
# ==============================

def expenditure_create(request):

    if request.method == 'POST':

        form = ExpenditureForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('expenditure_list')

    else:

        form = ExpenditureForm()

    context = {
        'form': form
    }

    return render(
        request,
        'expenditure_form.html',
        context
    )


# ==============================
# EXPENDITURE REPORTS
# ==============================

def expenditure_reports(request):

    report_type = request.GET.get('report_type')

    category = request.GET.get('category')

    expenses = Expenditure.objects.all().order_by('-date')

    today = now().date()

    current_month = today.month

    current_year = today.year

    # ==========================
    # DAILY REPORT
    # ==========================

    if report_type == 'daily':

        expenses = expenses.filter(
            date=today
        )

    # ==========================
    # MONTHLY REPORT
    # ==========================

    elif report_type == 'monthly':

        expenses = expenses.filter(
            date__month=current_month,
            date__year=current_year
        )

    # ==========================
    # CATEGORY REPORT
    # ==========================

    elif report_type == 'category':

        if category:

            expenses = expenses.filter(
                category=category
            )

    # ==========================
    # ANNUAL REPORT
    # ==========================

    elif report_type == 'annual':

        expenses = expenses.filter(
            date__year=current_year
        )

    # ==========================
    # TOTAL CALCULATION
    # ==========================

    total = expenses.aggregate(
        total_amount=Sum('amount')
    )['total_amount']

    # ==========================
    # CONTEXT
    # ==========================

    context = {

        'expenses': expenses,

        'total': total,

        'report_type': report_type,

        'current_month': current_month,

        'current_year': current_year,

        'categories': [

            'Salary',

            'Maintenance',

            'Program',

            'Utility',

            'Other'
        ]
    }

    return render(
        request,
        'expenditure_reports.html',
        context
    )