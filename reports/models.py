from django.db import models

# Create your models here.
from django.db import models

from sales.models import Sale

from inventory.models import Product

from deposists.models import Deposit


# =========================
# DAILY SALES REPORT
# =========================
class DailySalesReport(models.Model):

    date = models.DateField(
        auto_now_add=True
    )

    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    number_of_sales = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Daily Report - {self.date}"


# =========================
# STOCK ALERT REPORT
# =========================
class StockAlert(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity_remaining = models.PositiveIntegerField()

    alert_level = models.PositiveIntegerField(
        default=5
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.product.name


# =========================
# PENDING PAYMENT REPORT
# =========================
class PendingPayment(models.Model):

    customer_name = models.CharField(
        max_length=100
    )

    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=(

            ('pending', 'Pending'),

            ('paid', 'Paid'),

        ),
        default='pending'
    )

    due_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.customer_name


# =========================
# TRANSPORT REPORT
# =========================
class TransportReport(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE
    )

    customer_location = models.CharField(
        max_length=200
    )

    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    transport_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.sale.customer_name




    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.week_start} - {self.week_end}"


# =========================
# MONTHLY SALES REPORT
# =========================
class MonthlySalesReport(models.Model):

    month = models.CharField(
        max_length=20
    )

    year = models.PositiveIntegerField()

    total_sales = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    total_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.month} {self.year}"