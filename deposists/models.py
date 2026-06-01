from django.db import models
from sales.models import Sale
from sales.models import Customer

# DEPOSIT ACCOUNT
class Deposit(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='deposits')
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name='deposit')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    first_payment_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer.name} - {self.balance}"

# PAYMENT HISTORY
class DepositPayment(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField( auto_now_add=True)
    def __str__(self):
        return f"{self.deposit.customer.name} - {self.amount}"