from django.db import models
from django.core.validators import RegexValidator



class Supplier(models.Model):

    phone_validator = RegexValidator(
        regex=r'^(07\d{8}|2567\d{8})$',
        message='Enter valid Ugandan phone number'
    )

    STATUS = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    )

    company_name = models.CharField(
        max_length=255
    )

    contact_person = models.CharField(
        max_length=255
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[phone_validator]
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=255
    )

    product_supplied = models.CharField(
        max_length=255
    )

    total_supplied_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.company_name


# =========================
# SUPPLIER PAYMENTS
# =========================
class SupplierPayment(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.supplier.company_name} - {self.amount}"