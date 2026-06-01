from django import forms
from .models import DepositPayment


class DepositPaymentForm(forms.ModelForm):

    class Meta:

        model = DepositPayment

        fields = ['amount']

        widgets = {

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payment amount'
            })

        }