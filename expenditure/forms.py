from django import forms
from .models import Expenditure


class ExpenditureForm(forms.ModelForm):

    class Meta:
        model = Expenditure

        fields = [
            'date',
            'category',
            'amount',
            'description',
            'approved_by',
            'payment_mode'
        ]

        widgets = {

            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter amount'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter description'
                }
            ),

            'approved_by': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Approved by'
                }
            ),

            'payment_mode': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }