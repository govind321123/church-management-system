from django import forms
from .models import Household,Member,DeathRecord,BirthRecord
from datetime import date 
from django.core.exceptions import ValidationError



class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = [
    'locality',
    'house_number',
    'head_name',
    'gender',
    'address',
    'registration_date',
    'status'
]

        widgets = {
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'head_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

class MemberForm(forms.ModelForm):
    custom_relationship = forms.CharField(
    required=False,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom relationship'
        }
    )
)
    class Meta:
        model = Member
        fields = [
            'name', 'gender', 'dob', 'phone',
            'relationship',
            'baptism_status', 'baptism_date',
            'confirmation_status',
            'membership_status',
            'qualification',
            'occupation',
            'marital_status',
            'blood_group',
            'skills',
            'remarks'
           ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

            # 🔥 CHANGE THESE TO SELECT
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'relationship': forms.Select(attrs={'class': 'form-control'}),
            'membership_status': forms.Select(attrs={'class': 'form-control'}),

            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

            'baptism_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'baptism_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'confirmation_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),

            'occupation': forms.TextInput(attrs={'class': 'form-control'}),

            'marital_status': forms.Select(attrs={'class': 'form-control'}),

            'blood_group': forms.Select(attrs={'class': 'form-control'}),

            'skills': forms.TextInput(attrs={'class': 'form-control'}),

            'remarks': forms.Textarea(attrs={'class': 'form-control'}),


        }
        

class DeathForm(forms.ModelForm):

    class Meta:
        model = DeathRecord

        fields = [
            'member',
            'date_of_death',
            'cause_of_death',
            'funeral_date',
            'remarks',
            'death_certificate'
        ]

        widgets = {

            'member': forms.Select(attrs={
                'class': 'form-control'
            }),

            'date_of_death': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'cause_of_death': forms.Textarea(attrs={
                'class': 'form-control'
            }),

            'funeral_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'remarks': forms.Textarea(attrs={
                'class': 'form-control'
            }),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['member'].queryset = Member.objects.filter(
            is_active=True
        )
# class DeathForm(forms.ModelForm):
#     class Meta:
#         model = DeathRecord
#         fields = [
#             'member',
#             'date_of_death',
#             'cause_of_death',
#             'funeral_date',
#             'remarks',
#             'death_certificate'
#         ]

#         widgets = {
#             'member': forms.Select(attrs={'class': 'form-control'}),
#             'date_of_death': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'cause_of_death': forms.Textarea(attrs={'class': 'form-control'}),
#             'funeral_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'remarks': forms.Textarea(attrs={'class': 'form-control'}),
#         }

class BirthRecordForm(forms.ModelForm):

    custom_relationship = forms.CharField(

    required=False,

    widget=forms.TextInput(attrs={

        'class': 'form-control',

        'placeholder': 'Enter custom relationship'

    })

)

    class Meta:

        model = BirthRecord

        fields = [

            'household',
            'name',
            'gender',
            'dob',

            'father_name',
            'mother_name',

            'father_phone',
            'mother_phone',

            'relationship',

            'baptism_status',

            'birth_certificate'

        ]

        widgets = {

            'household': forms.Select(attrs={
                'class': 'form-control'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),

            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'father_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'mother_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'father_phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'mother_phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'relationship': forms.Select(attrs={
                'class': 'form-control'
            }),

            'baptism_status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'birth_certificate': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

        }

    def clean_dob(self):

        dob = self.cleaned_data['dob']

        if dob > date.today():

            raise ValidationError(
                "Date of birth cannot be future date."
            )

        return dob

