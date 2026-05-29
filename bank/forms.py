from django import forms
from .models import (
    BankAccount,
    BankTransaction
)


# ======================================
# BANK ACCOUNT FORM
# ======================================

class BankAccountForm(forms.ModelForm):

    class Meta:

        model = BankAccount

        fields = [
            'account_name',
            'bank_name',
            'account_number',
            'ifsc_code',
            'opening_balance'
        ]

        widgets = {

            'account_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Account Name'
                }
            ),

            'bank_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Bank Name'
                }
            ),

            'account_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Account Number'
                }
            ),

            'ifsc_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter IFSC Code'
                }
            ),

            'opening_balance': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Opening Balance'
                }
            ),

        }


# ======================================
# DEPOSIT FORM
# ======================================

class DepositForm(forms.ModelForm):

    class Meta:

        model = BankTransaction

        fields = [
            'bank_account',
            'date',
            'amount',
            'source',
            'remarks'
        ]

        widgets = {

            'bank_account': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Amount'
                }
            ),

            'source': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Remarks'
                }
            ),

        }


# ======================================
# WITHDRAWAL FORM
# ======================================

class WithdrawalForm(forms.ModelForm):

    class Meta:

        model = BankTransaction

        fields = [
            'bank_account',
            'date',
            'amount',
            'purpose',
            'remarks'
        ]

        widgets = {

            'bank_account': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Amount'
                }
            ),

            'purpose': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter Purpose'
                }
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Remarks'
                }
            ),

        }