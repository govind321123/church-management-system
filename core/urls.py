from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (

    home,

    add_household,
    edit_household,
    delete_household,
    household_detail,

    add_member,
    member_detail,
    edit_member,
    delete_member,

    add_death,
    death_list,

    add_birth,
    birth_list,
    delete_birth,

    demographic_report,
    spiritual_report,
    household_report,
    combined_report,
    reports_page,

    export_death_pdf,
    export_death_excel,

    offering_list,
    add_offering,
    edit_offering,
    delete_offering,
    offering_reports,

    CustomLoginView,

)

urlpatterns = [

    # =========================================
    # HOME
    # =========================================

    path(
        '',
        home,
        name='home'
    ),

    # =========================================
    # HOUSEHOLD
    # =========================================

    path(
        'add-household/',
        add_household,
        name='add_household'
    ),

    path(
        'household/<int:id>/',
        household_detail,
        name='household_detail'
    ),

    path(
        'household/edit/<int:id>/',
        edit_household,
        name='edit_household'
    ),

    path(
        'household/delete/<int:id>/',
        delete_household,
        name='delete_household'
    ),

    # =========================================
    # MEMBER
    # =========================================

    path(
        'household/<int:household_id>/add-member/',
        add_member,
        name='add_member'
    ),

    path(
        'member/<int:id>/',
        member_detail,
        name='member_detail'
    ),

    path(
        'member/edit/<int:id>/',
        edit_member,
        name='edit_member'
    ),

    path(
        'member/delete/<int:id>/',
        delete_member,
        name='delete_member'
    ),

    # =========================================
    # DEATH
    # =========================================

    path(
        'add-death/',
        add_death,
        name='add_death'
    ),

    path(
        'death-list/',
        death_list,
        name='death_list'
    ),

    # =========================================
    # BIRTH
    # =========================================

    path(
        'birth/add/',
        add_birth,
        name='add_birth'
    ),

    path(
        'birth/list/',
        birth_list,
        name='birth_list'
    ),

    path(
        'birth/delete/<int:id>/',
        delete_birth,
        name='delete_birth'
    ),

    # =========================================
    # REPORTS
    # =========================================

    path(
        'reports/',
        reports_page,
        name='reports_page'
    ),

    path(
        'reports/demographic/',
        demographic_report,
        name='demographic_report'
    ),

    path(
        'reports/spiritual/',
        spiritual_report,
        name='spiritual_report'
    ),

    path(
        'reports/household/',
        household_report,
        name='household_report'
    ),

    path(
        'reports/combined/',
        combined_report,
        name='combined_report'
    ),

    # =========================================
    # EXPORTS
    # =========================================

    path(
        'export/death/pdf/',
        export_death_pdf,
        name='export_death_pdf'
    ),

    path(
        'export/death/excel/',
        export_death_excel,
        name='export_death_excel'
    ),

    # =========================================
    # OFFERINGS
    # =========================================

    path(
        'offerings/',
        offering_list,
        name='offering_list'
    ),

    path(
        'offerings/add/',
        add_offering,
        name='add_offering'
    ),

    path(
        'offerings/edit/<int:id>/',
        edit_offering,
        name='edit_offering'
    ),

    path(
        'offerings/delete/<int:id>/',
        delete_offering,
        name='delete_offering'
    ),

    path(
        'offering-reports/',
        offering_reports,
        name='offering_reports'
    ),

    # =========================================
    # AUTHENTICATION
    # =========================================

    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(
            next_page='login'
        ),
        name='logout'
    ),

]