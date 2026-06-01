from django import forms

from .models import Supplier
from .models import SupplierPayment

class SupplierForm(forms.ModelForm):

    class Meta:

        model = Supplier

        fields = '__all__'

        widgets = {

            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

        }

from .models import SupplierPayment


class SupplierPaymentForm(forms.ModelForm):

    class Meta:

        model = SupplierPayment

        fields = ['amount']

        widgets = {

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payment amount'
            })

        }





class SupplierPaymentForm(forms.ModelForm):

    class Meta:

        model = SupplierPayment

        fields = ['amount']

        widgets = {

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payment amount'
            })

        }
              