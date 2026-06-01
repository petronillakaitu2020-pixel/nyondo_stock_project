from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from .forms import SupplierPaymentForm


def update_supplier_balance(supplier):

    total_paid = sum(

        payment.amount

        for payment in supplier.payments.all()

    )

    supplier.amount_paid = total_paid

    supplier.balance = (
        supplier.total_supplied_amount
        - total_paid
    )

    if supplier.balance <= 0:

        supplier.payment_status = 'paid'

    else:

        supplier.payment_status = 'pending'

    supplier.save()
# =========================
# SUPPLIER LIST
# =========================
def supplier_list(request):

    suppliers = Supplier.objects.all().order_by('-created_at')

    return render(request, 'supplier_list.html', {
        'suppliers': suppliers
    })


# =========================
# ADD SUPPLIER
# =========================
def add_supplier(request):

    form = SupplierForm(request.POST or None)

    if form.is_valid():

        form.save()

        return redirect('supplier_list')

    return render(request, 'add_supplier.html', {
        'form': form
    })


# =========================
# SUPPLIER DETAIL
# =========================
def supplier_detail(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    return render(request, 'supplier_details.html', {
        'supplier': supplier
    })


# =========================
# EDIT SUPPLIER
# =========================
def edit_supplier(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    form = SupplierForm(
        request.POST or None,
        instance=supplier
    )

    if form.is_valid():

        form.save()

        return redirect('supplier_list')

    return render(request, 'edit_supplier.html', {
        'form': form
    })


# =========================
# DELETE SUPPLIER
# =========================
def delete_supplier(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    if request.method == "POST":

        supplier.delete()

        return redirect('supplier_list')

    return render(request, 'delete_supplier.html', {
        'supplier': supplier
    })

# =========================
# ADD PAYMENT
# =========================
def add_supplier_payment(request, id):

    supplier = get_object_or_404(
        Supplier,
        id=id
    )

    form = SupplierPaymentForm(
        request.POST or None
    )

    if form.is_valid():

        payment = form.save(commit=False)

        payment.supplier = supplier

        payment.save()

        update_supplier_balance(supplier)

        return redirect('supplier_list')

    return render(
        request,
        'add_supplier_payment.html',
        {
            'form': form,
            'supplier': supplier
        }
    )