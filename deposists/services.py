from .models import Deposit
# CREATE DEPOSIT RECORD
def create_deposit(sale):
    if (sale.payment_method == "credit"and sale.balance > 0):
        Deposit.objects.create(
            customer=sale.customer,
            sale=sale,
            total_amount=sale.final_total,
            amount_paid=sale.amount_paid,
            balance=sale.balance,
            status='pending'
        )

# UPDATE DEPOSIT STATUS
def update_deposit(deposit):
    total_paid = sum(payment.amount for payment in deposit.payments.all())
    deposit.amount_paid = total_paid
    deposit.balance = deposit.total_amount - total_paid
    if deposit.balance <= 0:
        deposit.status = 'paid'
    else:
        deposit.status = 'pending'
    deposit.save()

    sale = deposit.sale
    if sale:
        sale.amount_paid = total_paid
        sale.balance = sale.final_total - total_paid
        sale.status = deposit.status
        sale.save()