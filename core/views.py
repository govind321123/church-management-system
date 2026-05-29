
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q, Count, Sum
from django.db.models.functions import ExtractYear, ExtractMonth

from django.http import HttpResponse

from reportlab.pdfgen import canvas
import openpyxl
from datetime import date

from expenditure.models import Expenditure
from bank.models import BankAccount

from .models import (
    Household,
    Member,
    BirthRecord,
    DeathRecord,
    Offering,
    OfferingCategory
)

from .forms import (

    HouseholdForm,
    MemberForm,
    BirthRecordForm,
    DeathForm
)

# =====================================================
# HOME / DASHBOARD
# =====================================================

@login_required
def home(request):

    # ==========================================
    # BASE QUERYSETS
    # ==========================================

    households = Household.objects.all()

    members = Member.objects.filter(
        is_deceased=False,
        is_active=True
    )

    # ==========================================
    # SEARCH & FILTER
    # ==========================================

    search_query = request.GET.get('search')

    gender = request.GET.get('gender')

    baptism = request.GET.get('baptism')

    age_filter = request.GET.get('age')

    # SEARCH

    if search_query:

        members = members.filter(

            Q(name__icontains=search_query) |

            Q(phone__icontains=search_query) |

            Q(household__locality__icontains=search_query)

        )

    # GENDER FILTER

    if gender:

        members = members.filter(
            gender=gender
        )

    # BAPTISM FILTER

    if baptism == 'Yes':

        members = members.filter(
            baptism_status=True
        )

    elif baptism == 'No':

        members = members.filter(
            baptism_status=False
        )

    # ==========================================
    # AGE FILTER
    # ==========================================

    filtered_members = []

    for m in members:

        age = m.age

        if age_filter == 'below_14' and age < 14:

            filtered_members.append(m)

        elif age_filter == 'below_18' and age < 18:

            filtered_members.append(m)

        elif age_filter == 'above_18' and age >= 18:

            filtered_members.append(m)

        elif not age_filter:

            filtered_members.append(m)

    members = filtered_members

    # ==========================================
    # COUNTS
    # ==========================================

    total_members = len(members)

    total_households = households.count()

    deceased_count = Member.objects.filter(
        is_deceased=True
    ).count()

    recent_deaths = Member.objects.filter(
        is_deceased=True
    ).order_by('-id')[:5]

    male_count = len([
        m for m in members
        if m.gender == 'Male'
    ])

    female_count = len([
        m for m in members
        if m.gender == 'Female'
    ])

    baptized = len([
        m for m in members
        if m.baptism_status
    ])

    not_baptized = len([
        m for m in members
        if not m.baptism_status
    ])

    below_14 = len([
        m for m in members
        if m.age < 14
    ])

    below_18 = len([
        m for m in members
        if 14 <= m.age < 18
    ])

    above_18 = len([
        m for m in members
        if m.age >= 18
    ])

    # ==========================================
    # FINANCIAL SUMMARY
    # ==========================================

    today = date.today()

    current_month_offering = Offering.objects.filter(
        service_date__month=today.month,
        service_date__year=today.year
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    current_month_expense = Expenditure.objects.filter(
        date__month=today.month,
        date__year=today.year
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    bank_accounts = BankAccount.objects.all()

    current_bank_balance = sum(
        account.current_balance
        for account in bank_accounts
    )

    # ==========================================
    # RENDER
    # ==========================================

    return render(request, 'index.html', {

        'households': households,
        'members': members,

        'total_members': total_members,
        'total_households': total_households,

        'male_count': male_count,
        'female_count': female_count,

        'baptized': baptized,
        'not_baptized': not_baptized,

        'below_14': below_14,
        'below_18': below_18,
        'above_18': above_18,

        'deceased_count': deceased_count,
        'recent_deaths': recent_deaths,

        'current_month_offering': current_month_offering,
        'current_month_expense': current_month_expense,
        'current_bank_balance': current_bank_balance,

    })

# =====================================================
# HOUSEHOLD
# =====================================================
@login_required
def add_household(request):

    if request.method == 'POST':

        form = HouseholdForm(request.POST)

        if form.is_valid():

            household = form.save()

            # AUTO CREATE MEMBER
            Member.objects.create(

                household=household,

                name=household.head_name,

                gender=household.gender,

                dob='2000-01-01',

                relationship='Father'
                if household.gender == 'Male'
                else 'Mother',

                membership_status='Believer'
            )

            messages.success(
                request,
                "Household added successfully!"
            )

            return redirect('home')

    else:

        form = HouseholdForm()

    return render(request, 'add_household.html', {
        'form': form
    })



@login_required
def edit_household(request, id):

    household = get_object_or_404(
        Household,
        id=id
    )

    if request.method == 'POST':

        form = HouseholdForm(
            request.POST,
            instance=household
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Household updated successfully!"
            )

            return redirect(
                'household_detail',
                id=household.id
            )

    else:

        form = HouseholdForm(
            instance=household
        )

    return render(request, 'edit_household.html', {

        'form': form,
        'household': household

    })


@login_required
def delete_household(request, id):

    household = get_object_or_404(
        Household,
        id=id
    )

    if request.method == 'POST':

        household.delete()

        messages.success(
            request,
            "Household deleted successfully!"
        )

        return redirect('home')

    return render(request, 'delete_household.html', {

        'household': household

    })


@login_required
def household_detail(request, id):

    household = get_object_or_404(
        Household,
        id=id
    )

    # members = household.members.filter(
    #     is_deceased=False
    # )

    members = household.members.filter(
    is_active=True
)

    return render(request, 'household_detail.html', {

        'household': household,
        'members': members

    })


# =====================================================
# MEMBER
# =====================================================

@login_required
def add_member(request, household_id):

    household = get_object_or_404(
        Household,
        id=household_id
    )

    if request.method == 'POST':

        form = MemberForm(request.POST)

        # if form.is_valid():

        #     member = form.save(commit=False)

        #     member.household = household

        #     member.save()
        if form.is_valid():

            member = form.save(commit=False)

            # HANDLE CUSTOM RELATIONSHIP
            relationship = form.cleaned_data.get('relationship')

            custom_relationship = form.cleaned_data.get(
                'custom_relationship'
            )

            if relationship == 'Other' and custom_relationship:

                member.relationship = custom_relationship

            else:

                member.relationship = relationship

            member.household = household

            member.save()

            messages.success(
                request,
                "Member added successfully!"
            )

            return redirect(
                'household_detail',
                id=household.id
            )

    else:
        form = MemberForm()

    return render(request, 'add_member.html', {

        'form': form,
        'household': household

    })


@login_required
def member_detail(request, id):

    member = get_object_or_404(
        Member,
        id=id
    )

    return render(request, 'member_detail.html', {

        'member': member

    })


# =====================================================
# DEATH
# =====================================================

@login_required
def add_death(request):

    if request.method == 'POST':

        form = DeathForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Death record added successfully!"
            )

            return redirect('home')

    else:
        form = DeathForm()

    return render(request, 'add_death.html', {
        'form': form
    })


@login_required
def death_list(request):

    records = DeathRecord.objects.select_related(
        'member'
    ).all()

    # SEARCH

    search = request.GET.get('search')

    if search:

        records = records.filter(
            member__name__icontains=search
        )

    # YEAR FILTER

    year = request.GET.get('year')

    if year:

        records = records.filter(
            date_of_death__year=year
        )

    # MONTH FILTER

    month = request.GET.get('month')

    if month:

        records = records.filter(
            date_of_death__month=month
        )

    # SUMMARY

    total_deaths = DeathRecord.objects.count()

    year_summary = DeathRecord.objects.annotate(
        year=ExtractYear('date_of_death')
    ).values('year').annotate(
        total=Count('id')
    ).order_by('-year')

    month_summary = DeathRecord.objects.annotate(
        month=ExtractMonth('date_of_death')
    ).values('month').annotate(
        total=Count('id')
    ).order_by('month')

    years = DeathRecord.objects.annotate(
        year=ExtractYear('date_of_death')
    ).values_list(
        'year',
        flat=True
    ).distinct().order_by('-year')

    records = records.order_by(
        '-date_of_death'
    )

    return render(request, 'death_list.html', {

        'records': records,
        'years': years,
        'total_deaths': total_deaths,
        'year_summary': year_summary,
        'month_summary': month_summary,

    })


# =====================================================
# new birth record also creates a new member
# =====================================================

# =====================================================
# BIRTH
# =====================================================

from django.db import transaction

@login_required
def add_birth(request):

    if request.method == 'POST':

        form = BirthRecordForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            with transaction.atomic():

                birth = form.save(commit=False)

                # =====================================
                # HANDLE BABY NAME
                # =====================================

                baby_name = (

                    birth.name

                    if birth.name

                    else f"B/O {birth.mother_name}"

                )

                # =====================================
                # HANDLE CUSTOM RELATIONSHIP
                # =====================================

                relationship = form.cleaned_data.get(
                    'relationship'
                )

                custom_relationship = form.cleaned_data.get(
                    'custom_relationship'
                )

                if (
                    relationship == 'Other'
                    and custom_relationship
                ):

                    final_relationship = custom_relationship

                else:

                    final_relationship = relationship

                # =====================================
                # CREATE MEMBER
                # =====================================

                member = Member.objects.create(

                    household=birth.household,

                    name=baby_name,

                    gender=birth.gender,

                    dob=birth.dob,

                    phone=(

                        birth.father_phone

                        or birth.mother_phone

                    ),

                    relationship=final_relationship,

                    baptism_status=birth.baptism_status,

                    membership_status='Visitor'

                )

                birth.member = member

                # SAVE CUSTOM RELATIONSHIP
                birth.relationship = final_relationship

                birth.save()

            messages.success(

                request,

                "Birth record added successfully!"

            )

            return redirect('birth_list')

    else:

        form = BirthRecordForm()

    return render(request, 'add_birth.html', {

        'form': form

    })


@login_required
def birth_list(request):

    query = request.GET.get('q')

    births = BirthRecord.objects.select_related(
        'household',
        'member'
    )

    if query:

        births = births.filter(

            Q(name__icontains=query) |

            Q(father_name__icontains=query) |

            Q(mother_name__icontains=query) |

            Q(father_phone__icontains=query) |

            Q(mother_phone__icontains=query) |

            Q(household__head_name__icontains=query) |

            Q(household__locality__icontains=query) |

            Q(household__household_id__icontains=query)

        )

    births = births.order_by('-created_at')

    return render(request, 'birth_list.html', {

        'births': births,
        'query': query

    })


@login_required
def delete_birth(request, id):

    birth = get_object_or_404(
        BirthRecord,
        id=id
    )

    if request.method == 'POST':

        member = birth.member

        birth.delete()

        if member:
            member.delete()

        messages.success(
            request,
            "Birth record deleted successfully!"
        )

        return redirect('birth_list')

    return render(request, 'confirm_delete.html', {
        'birth': birth
    })


# # =====================================================
# # BIRTH
# # =====================================================






# @login_required
# def add_birth(request):

#     if request.method == 'POST':

#         form = BirthRecordForm(
#             request.POST,
#             request.FILES
#         )

#         if form.is_valid():

#             birth = form.save(commit=False)

#             # CREATE MEMBER

#             member = Member.objects.create(

#                 household=birth.household,

#                 name=birth.name
#                 if birth.name else "B/O",

#                 gender=birth.gender,

#                 dob=birth.dob,

#                 phone=birth.parent_phone,

#                 relationship=birth.relationship,

#                 baptism_status=False,

#                 membership_status='Believer'

#             )

#             birth.member = member

#             birth.save()

#             messages.success(
#                 request,
#                 "Birth record added successfully!"
#             )

#             return redirect('add_birth')

#     else:
#         form = BirthRecordForm()

#     return render(request, 'add_birth.html', {
#         'form': form
#     })


# @login_required
# def birth_list(request):

#     query = request.GET.get('q')

#     births = BirthRecord.objects.select_related(
#         'household',
#         'member'
#     )

#     if query:

#         births = births.filter(

#             Q(name__icontains=query) |
#             Q(parent_phone__icontains=query) |
#             Q(father_name__icontains=query) |
#             Q(mother_name__icontains=query)

#         )

#     births = births.order_by('-created_at')

#     return render(request, 'birth_list.html', {

#         'births': births,
#         'query': query

#     })


# @login_required
# def delete_birth(request, id):

#     birth = BirthRecord.objects.get(id=id)

#     if request.method == 'POST':

#         birth.delete()

#         messages.success(
#             request,
#             "Birth record deleted successfully!"
#         )

#         return redirect('birth_list')

#     return render(request, 'confirm_delete.html', {
#         'birth': birth
#     })


# =====================================================
# REPORTS
# =====================================================

@login_required
def demographic_report(request):

    # members = Member.objects.filter(
    #     is_deceased=False
    # )

    members = Member.objects.filter(
    is_active=True
)

    total_members = members.count()

    male = members.filter(
        gender='Male'
    ).count()

    female = members.filter(
        gender='Female'
    ).count()

    below_14 = len([
        m for m in members
        if m.age < 14
    ])

    below_18 = len([
        m for m in members
        if 14 <= m.age < 18
    ])

    above_18 = len([
        m for m in members
        if m.age >= 18
    ])

    return render(request, 'demographic_report.html', {

        'total': total_members,
        'male': male,
        'female': female,
        'below_14': below_14,
        'below_18': below_18,
        'above_18': above_18

    })


@login_required
def spiritual_report(request):

    # members = Member.objects.filter(
    #     is_deceased=False
    # )

    members = Member.objects.filter(
    is_active=True
)

    baptized = members.filter(
        baptism_status=True
    ).count()

    not_baptized = members.filter(
        baptism_status=False
    ).count()

    believers = members.filter(
        membership_status='Believer'
    ).count()

    membership_counts = {

        'Believer': members.filter(
            membership_status='Believer'
        ).count(),

        'Catechumen': members.filter(
            membership_status='Catechumen'
        ).count(),

        'Visitor': members.filter(
            membership_status='Visitor'
        ).count(),

    }

    return render(request, 'spiritual_report.html', {

        'baptized': baptized,
        'not_baptized': not_baptized,
        'believers': believers,
        'membership_counts': membership_counts

    })


@login_required
def household_report(request):

    households = Household.objects.all()

    total_households = households.count()

    locality_counts = households.values(
        'locality'
    ).annotate(
        count=Count('id')
    )

    locality_houses = {}

    for h in households:

        locality_houses.setdefault(
            h.locality,
            []
        ).append(h.house_number)

    return render(request, 'household_report.html', {

        'total': total_households,
        'locality_counts': locality_counts,
        'locality_houses': locality_houses

    })


@login_required
def combined_report(request):

    members = Member.objects.filter(
        is_active=True
    )

    households = Household.objects.all()

    # =====================================
    # SPIRITUAL DATA
    # =====================================

    baptized = members.filter(
        baptism_status=True
    ).count()

    not_baptized = members.filter(
        baptism_status=False
    ).count()

    believers = members.filter(
        membership_status='Believer'
    ).count()

    catechumen = members.filter(
        membership_status='Catechumen'
    ).count()

    visitors = members.filter(
        membership_status='Visitor'
    ).count()

    # =====================================
    # HOUSEHOLD DATA
    # =====================================

    total_households = households.count()

    locality_counts = households.values(
        'locality'
    ).annotate(
        count=Count('id')
    )

    locality_houses = {}

    for h in households:

        locality_houses.setdefault(
            h.locality,
            []
        ).append(h.house_number)

    context = {

        # Spiritual
        'baptized': baptized,
        'not_baptized': not_baptized,
        'believers': believers,
        'catechumen': catechumen,
        'visitors': visitors,

        # Household
        'total_households': total_households,
        'locality_counts': locality_counts,
        'locality_houses': locality_houses,

    }

    return render(
        request,
        'combined_report.html',
        context
    )


@login_required
def reports_page(request):

    return render(request, 'reports.html')


# =====================================================
# EXPORTS
# =====================================================

@login_required
def export_death_excel(request):

    wb = openpyxl.Workbook()

    ws = wb.active

    ws.title = "Death Records"

    ws.append([
        'Name',
        'Household',
        'Date of Death',
        'Funeral Date',
        'Cause'
    ])

    records = DeathRecord.objects.select_related(
        'member'
    ).all()

    for r in records:

        ws.append([

            r.member.name,
            r.member.household.head_name,
            str(r.date_of_death),
            str(r.funeral_date),
            r.cause_of_death

        ])

    response = HttpResponse(
        content_type='application/ms-excel'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="death_records.xlsx"'

    wb.save(response)

    return response


@login_required
def export_death_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="death_records.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        200,
        y,
        "Death Records Report"
    )

    y -= 40

    p.setFont("Helvetica", 10)

    records = DeathRecord.objects.select_related(
        'member'
    ).all()

    for r in records:

        text = f"{r.member.name} | {r.date_of_death} | {r.cause_of_death}"

        p.drawString(50, y, text)

        y -= 20

        if y < 50:

            p.showPage()

            y = 800

    p.save()

    return response


# =====================================================
# LOGIN
# =====================================================

class CustomLoginView(LoginView):

    template_name = 'login.html'


@login_required
def edit_member(request, id):

    member = get_object_or_404(Member, id=id)

    if request.method == 'POST':

        form = MemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()

            return redirect(
                'member_detail',
                id=member.id
            )

    else:

        form = MemberForm(instance=member)

    return render(request, 'edit_member.html', {
        'form': form,
        'member': member
    })


@login_required
def delete_member(request, id):

    member = get_object_or_404(
        Member,
        id=id
    )

    if request.method == 'POST':

        member.is_active = False

        member.save()

        messages.success(
            request,
            "Member deleted successfully!"
        )

    return redirect(
        'household_detail',
        id=member.household.id
    )


@login_required
def offering_list(request):

    offerings = Offering.objects.all().order_by('-id')

    context = {
        'offerings': offerings
    }

    return render(
    request,
    'offering_list.html',
    context
)



@login_required
def add_offering(request):

    categories = OfferingCategory.objects.all()

    if request.method == 'POST':

        category_id = request.POST.get('category')

        custom_category = request.POST.get(
            'custom_category'
        )

        amount = request.POST.get('amount')

        given_by = request.POST.get('given_by')

        payment_method = request.POST.get(
            'payment_method'
        )

        service_date = request.POST.get(
            'service_date'
        )

        remarks = request.POST.get('remarks')

        # =====================================
        # HANDLE CUSTOM CATEGORY
        # =====================================

        if custom_category:

            category, created = (
                OfferingCategory.objects.get_or_create(
                    name=custom_category
                )
            )

        else:

            category = OfferingCategory.objects.get(
                id=category_id
            )

        Offering.objects.create(

            category=category,

            amount=amount,

            given_by=given_by,

            payment_method=payment_method,

            service_date=service_date,

            remarks=remarks,

            created_by=request.user,

        )

        messages.success(
            request,
            'Offering added successfully'
        )

        return redirect('offering_list')

    context = {
        'categories': categories
    }

    return render(
        request,
        'add_offering.html',
        context
    )




def edit_offering(request, id):

    offering = Offering.objects.get(id=id)

    categories = OfferingCategory.objects.all()

    if request.method == 'POST':

        offering.category = OfferingCategory.objects.get(
            id=request.POST.get('category')
        )

        offering.amount = request.POST.get('amount')

        offering.given_by = request.POST.get('given_by')

        offering.payment_method = request.POST.get(
            'payment_method'
        )

        offering.service_date = request.POST.get(
            'service_date'
        )

        offering.remarks = request.POST.get('remarks')

        offering.save()

        messages.success(
            request,
            'Offering updated successfully'
        )

        return redirect('offering_list')

    context = {
        'offering': offering,
        'categories': categories
    }

    return render(
        request,
        'edit_offering.html',
        context
    )



def delete_offering(request, id):

    offering = Offering.objects.get(id=id)

    offering.delete()

    messages.success(
        request,
        'Offering deleted successfully'
    )

    return redirect('offering_list')


@login_required
def offering_reports(request):

    offerings = Offering.objects.all()

    # FILTERS

    # date = request.GET.get('date')
    # month = request.GET.get('month')
    # year = request.GET.get('year')
    # category = request.GET.get('category')

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    date = request.GET.get('date')
    month = request.GET.get('month')
    year = request.GET.get('year')

    category = request.GET.get('category')

    if date:
        offerings = offerings.filter(
            service_date=date
        )

    # DATE RANGE FILTER

    if from_date and to_date:

        offerings = offerings.filter(
            service_date__range=[
                from_date,
                to_date
            ]
        )

    elif from_date:

        offerings = offerings.filter(
            service_date__gte=from_date
        )

    elif to_date:

        offerings = offerings.filter(
            service_date__lte=to_date
        )

    if month:
        offerings = offerings.filter(
            service_date__month=month
        )

    if year:
        offerings = offerings.filter(
            service_date__year=year
        )

    if category:
        offerings = offerings.filter(
            category_id=category
        )

    # TOTAL

    total_amount = offerings.aggregate(
        total=Sum('amount')
    )['total'] or 0

    categories = OfferingCategory.objects.all()

    context = {
        'offerings': offerings.order_by('-service_date'),
        'categories': categories,
        'total_amount': total_amount
    }

    return render(
        request,
        'offering_reports.html',
        context
    )
