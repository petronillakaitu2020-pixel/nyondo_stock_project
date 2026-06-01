from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Deposit
from .models import DepositPayment
from .forms import DepositPaymentForm
from .services import update_deposit

# ALL DEPOSITS
def deposit_list(request):
    deposits = Deposit.objects.all().order_by('-created_at')
    return render(request, 'deposit_list.html', {'deposits': deposits})

# DEPOSIT DETAILS
def deposit_detail(request, id):
    deposit = get_object_or_404(Deposit, id=id)
    payments = deposit.payments.all()
    return render(request, 'deposit_details.html', {
        'deposit': deposit,
        'payments': payments
    })


# ADD PAYMENT

def add_payment(request, id):
    deposit = get_object_or_404(Deposit, id=id)
    form = DepositPaymentForm(request.POST or None)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.deposit = deposit
        payment.save()
        # update balances
        update_deposit(deposit)
        # redirect to receipt
        return redirect(
            'payment_receipt',
            payment.id
        )

    return render(request, 'add_payment.html', {
        'form': form,
        'deposit': deposit
    })


# DELETE DEPOSIT
def delete_deposit(request, id):
    deposit = get_object_or_404(Deposit, id=id)
    if request.method == "POST":
        deposit.delete()
        return redirect('deposit_list')
    return render(request, 'delete_deposit.html', {'deposit': deposit})


# PAYMENT RECEIPT
def payment_receipt(request, id):
    payment = get_object_or_404(DepositPayment, id=id)
    deposit = payment.deposit
    return render(request,'payment_receipt.html',{
            'payment': payment,
            'deposit':deposit
        }
    )