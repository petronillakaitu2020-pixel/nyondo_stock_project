from django.db import models
from django.conf import settings
from suppliers.models import Supplier


class Product(models.Model):

    PRODUCT_NAMES = (

        ('cement', 'Cement'),
        ('iron_bar', 'Iron Bar'),
        ('nails', 'Nails'),
        ('wire_mesh', 'Wire Mesh'),
        ('barbed_wire', 'Barbed Wire'),
        ('iron_sheet', 'Iron Sheet'),
        ('wheelbarrow', 'Wheelbarrow'),
        ('paint', 'Paint'),

    )

    SPECIFICATION_CHOICES = (

        ('cem iiN', 'cem iiN Cement'),
        ('cem iiiN', 'cem iiiN Cement'),
        ('10mm', '10mm Iron Bar'),
        ('12mm', '12mm Iron Bar'),
        ('16mm', '16mm Iron Bar'),
        ('27gauge', '27 Gauge'),
        ('28gauge', '28 Gauge'),
        ('high_tensile', 'High Tensile'),
        ('low_tensile', 'Low Tensile'),

    )

    COLOR_CHOICES = (

        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('black', 'Black'),
        ('white', 'White'),
        ('silver', 'Silver'),

    )

    UNIT_CHOICES = (

        ('piece', 'Piece'),
        ('kg', 'Kilogram'),
        ('bundle', 'Bundle'),
        ('roll', 'Roll'),
        ('box', 'Box'),
        ('bag', 'Bag'),

    )


    # PRODUCT DETAILs

    product_name = models.CharField(max_length=50, choices=PRODUCT_NAMES)
    specification = models.CharField(max_length=100, choices=SPECIFICATION_CHOICES)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    buying_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)


    # STOCK

    quantity = models.PositiveIntegerField()
    available_stock = models.PositiveIntegerField(default=0)

    # RELATIONSHIPS

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):

        return f"{self.get_product_name_display()} ({self.get_specification_display()})"
    # CALCULATED TOTAL

   # @property
    #def total_amount(self):
     #   return self.quantity * self.selling_price
    # SAVE LOGIC

    def save(self, *args, **kwargs):
        # first time product is created
        if not self.pk:
            self.available_stock = self.quantity
        super().save(*args, **kwargs)
    