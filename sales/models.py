from django.db import models
from django.conf import settings
from inventory.models import Product


# =========================
# CUSTOMER
# =========================
class Customer(models.Model):

    CUSTOMER_TYPES = (
        ('walk_in', 'Walk In'),
        ('retailer', 'Retailer'),
        ('wholesaler', 'Wholesaler'),
    )

    name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


# SALE
class Sale(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('credit', 'Credit'),)

    STATUS = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    )
    
    invoice_no = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transport_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.invoice_no


# SALE ITEMS
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100, choices=Product.SPECIFICATION_CHOICES)
    color = models.CharField(max_length=50, choices=Product.COLOR_CHOICES, blank=True, null=True)
    unit = models.CharField(max_length=50, choices=Product.UNIT_CHOICES)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    def save(self, *args, **kwargs):
        # automatic unit price from inventory
        self.unit_price = self.product.selling_price
        # automatic details from inventory
        self.specification = self.product.specification
        self.color = self.product.color
        self.unit = self.product.unit
        # total
        self.total_price = self.unit_price * self.quantity
        # reduce stock
        self.product.available_stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.get_product_name_display()