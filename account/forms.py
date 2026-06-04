from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

# REGISTER FORM
# =========================
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'nin',
            'phone_number',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'nin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter NIN Number'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            
        }

    # VALIDATE NIN
    def clean_nin(self):
        nin = self.cleaned_data['nin']
        if len(nin) < 10:
            raise forms.ValidationError("NIN must be valid")
        return nin


    # VALIDATE PHONE
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.startswith(('07', '03')):
            raise forms.ValidationError(
                "Phone number must start with 07 or 03")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must have 10 digits")
        return phone


# LOGIN FORM
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password'
            })
    )