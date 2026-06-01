from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.utils import timezone
from .models import Customer, Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from inventory.models import Product
from deposists.models import Deposit


# SALES LIST
@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            customer_type = form.cleaned_data['customer_type']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            distance_km = form.cleaned_data['distance_km']
            payment_method = form.cleaned_data['payment_method']

            # CREATE CUSTOMER
            customer = Customer.objects.create(
                name=customer_name,
                customer_type=customer_type,
                phone=phone,
                location=location,
                distance_km=distance_km
            )

            # WALK-IN VALIDATION
            if customer_type == 'walk_in' and payment_method != 'cash':
                messages.error(
                    request,
                    'Walk-in customers must pay using cash.'
                )
                return redirect('create_sale')

            # GENERATE INVOICE
            invoice_no = f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}"

            # CREATE SALE
            sale = Sale.objects.create(
                invoice_no=invoice_no,
                customer=customer,
                payment_method=payment_method,
                amount_paid=0,
                created_by=request.user)
            return redirect('add_sale_items', sale.id)
    else:
        form = SaleForm()
    return render(request, 'create_sale.html', {'form': form})


# ADD SALE ITEMS
@login_required
def add_sale_items(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()
    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            # CHECK STOCK
            if quantity > product.available_stock:
                messages.error(
                    request,
                    f"Low stock alert! You tried to add {quantity} pcs, but only {product.available_stock} pcs remain."        
                )
                return redirect('add_sale_items', sale.id)
            
            else:
            # CREATE SALE ITEM
                sale_item = SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=product.selling_price,
                    total_price=product.selling_price * quantity)


            # REDUCE STOCK
            product.available_stock -= quantity
            product.save()


            # CALCULATE SUBTOTAL
            subtotal = sale.items.aggregate(
                total=Sum('total_price')
            )['total'] or Decimal('0')


            # TRANSPORT LOGIC
            if (sale.customer.distance_km <= 10 and subtotal >= 50000):
                transport_charge = Decimal('0')
            else:
                transport_charge = Decimal('30000')


            # FINAL TOTAL
            final_total = subtotal + transport_charge


            # BALANCE
            balance = final_total - sale.amount_paid


            # STATUS
            if balance <= 0:
                status = 'paid'
                balance = Decimal('0')
            else:
                status = 'pending'


            # UPDATE SALE
            sale.subtotal = subtotal
            sale.transport_charge = transport_charge
            sale.final_total = final_total
            sale.balance = balance
            sale.status = status
            sale.save()

            
            # AUTO CREATE DEPOSIT
            if sale.payment_method == 'credit':
                Deposit.objects.get_or_create(
                    customer=sale.customer,
                    sale=sale,
                    defaults={
                        'total_amount': sale.final_total,
                        'amount_paid': sale.amount_paid,
                        'balance': sale.balance,
                        'status': 'pending'})
            messages.success(request, 'Item added successfully.')
            return redirect('add_sale_items', sale.id)
    else:
        form = SaleItemForm()
    context = {
        'sale': sale,
        'items': items,
        'form': form
    }
    return render(request, 'add_sale_items.html', context)


# SALE RECEIPT
@login_required
def sale_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()
    context = {
        'sale': sale,
        'items': items}
    return render(request, 'sale_receipt.html', context)


@login_required
def sales_list(request):
    sales = Sale.objects.all().order_by('-created_at')
    context = {
        'sales': sales
    }
    return render(request, 'sales_list.html', context)

@login_required
def finalise_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        #get the actual amount paid from the cashier input
        amount_paid = request.POST.get('amount_paid', 0)
        amount_paid_decimal = Decimal(str(amount_paid))
        sale.amount_paid = amount_paid_decimal
        sale.balance = sale.final_total - amount_paid_decimal
        if sale.balance <= 0:
            sale.status = 'paid'
        else:
            sale.status = 'pending'
        sale.save()
        return redirect('sale_receipt', sale.id)
    return redirect('add_sale_items', sale_id=sale.id) 