from django.shortcuts import render

from inventory.models import Product

from sales.models import Sale

from deposists.models import Deposit

from suppliers.models import Supplier

from django.db.models import Sum

from datetime import timedelta
from django.utils import timezone


# =========================
# DASHBOARD
# =========================
def dashboard(request):

    today = timezone.now().date()

    week_ago = today - timedelta(days=7)

    # =========================
    # SALES
    # =========================
    today_sales = Sale.objects.filter(
        created_at__date=today
    )

    total_sales_today = today_sales.aggregate(
        Sum('final_total')
    )['final_total__sum'] or 0

    sales_count_today = today_sales.count()

    # =========================
    # WEEKLY PROFITS
    # =========================
    #weekly_sales = Sale.objects.filter(
       # created_at__date__gte=week_ago)



    # =========================
    # LOW STOCK
    # =========================
    low_stock_products = Product.objects.filter(
        quantity__lte=5
    )

    # =========================
    # PENDING DEPOSITS
    # =========================
    pending_deposits = Deposit.objects.filter(
        status='pending'
    )

    total_pending_debt = pending_deposits.aggregate(
        Sum('balance')
    )['balance__sum'] or 0

    # =========================
    # SUPPLIER BALANCES
    # =========================
    supplier_balances = Supplier.objects.filter(
        payment_status='pending'
    )

    total_supplier_balance = supplier_balances.aggregate(
        Sum('balance')
    )['balance__sum'] or 0

    # =========================
    # AVAILABLE PRODUCTS
    # =========================
    total_products = Product.objects.count()

    # =========================
    # RECENT SALES
    # =========================
    recent_sales = Sale.objects.order_by(
        '-created_at'
    )[:5]

    context = {

        'total_sales_today': total_sales_today,

        'sales_count_today': sales_count_today,


        'low_stock_products': low_stock_products,

        'pending_deposits': pending_deposits,

        'total_pending_debt': total_pending_debt,

        'supplier_balances': supplier_balances,

        'total_supplier_balance': total_supplier_balance,

        'total_products': total_products,

        'recent_sales': recent_sales,

    }

    return render(
        request,
        'dashboard.html',
        context
    )