
from django.db import models


# ==========================================
# PRODUCT MODEL
# ==========================================
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# ==========================================
# CUSTOMER ORDER MODEL
# ==========================================
class CustomerOrder(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(
        max_length=200
    )

    customer_location = models.CharField(
        max_length=255
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    order_date = models.DateField(
        auto_now_add=True
    )

    # NEW ORDER STATUS
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return (
            f"{self.customer_name} - "
            f"{self.product.name} - "
            f"{self.status}"
        )
