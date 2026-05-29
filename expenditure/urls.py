from django.urls import path
from . import views


urlpatterns = [

    # ==========================
    # EXPENDITURE LIST
    # ==========================

    path(
        '',
        views.expenditure_list,
        name='expenditure_list'
    ),

    # ==========================
    # ADD EXPENDITURE
    # ==========================

    path(
        'add/',
        views.expenditure_create,
        name='expenditure_add'
    ),

    # ==========================
    # EXPENDITURE REPORTS
    # ==========================

    path(
        'reports/',
        views.expenditure_reports,
        name='expenditure_reports'
    ),

]