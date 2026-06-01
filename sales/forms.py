from django import forms

from .models import SaleItem


# =====================================
# SALE FORM
# =====================================
class SaleForm(forms.Form):

    CUSTOMER_TYPES = (

        ('walk_in', 'Walk In'),
        ('retailer', 'Retailer'),
        ('wholesaler', 'Wholesaler'),
    )

    PAYMENT_METHODS = (

        ('cash', 'Cash'),
        ('credit', 'Credit'),
    )

    customer_name = forms.CharField(

        max_length=200,

        widget=forms.TextInput(attrs={

            'class': 'form-control',
            'placeholder': 'Enter customer name'
        })
    )

    customer_type = forms.ChoiceField(

        choices=CUSTOMER_TYPES,

        widget=forms.Select(attrs={

            'class': 'form-control'
        })
    )

    phone = forms.CharField(

        required=False,

        widget=forms.TextInput(attrs={

            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    location = forms.CharField(

        widget=forms.TextInput(attrs={

            'class': 'form-control',
            'placeholder': 'Customer location'
        })
    )

    distance_km = forms.DecimalField(

        widget=forms.NumberInput(attrs={

            'class': 'form-control',
            'placeholder': 'Distance in KM'
        })
    )

    payment_method = forms.ChoiceField(

        choices=PAYMENT_METHODS,

        widget=forms.Select(attrs={

            'class': 'form-control'
        })
    )

    amount_paid = forms.DecimalField(

        initial=0,

        widget=forms.NumberInput(attrs={

            'class': 'form-control'
        })
    )


# =====================================
# SALE ITEM FORM
# =====================================
class SaleItemForm(forms.ModelForm):

    class Meta:

        model = SaleItem

        fields = [

            'product',
            'specification',
            'color',
            'unit',
            'quantity'
        ]

        widgets = {

            'product': forms.Select(attrs={

                'class': 'form-select'
            }),

            'specification': forms.Select(attrs={
                'class': 'form-select',
                
            }),
            'color': forms.Select(attrs={
                'class': 'form-select',
                
            }),
            
            'unit': forms.Select(attrs={
                'class': 'form-select',
                
            }),

            'quantity': forms.NumberInput(attrs={

                'class': 'form-control',
                'placeholder': 'Enter quantity'
            }),
        }