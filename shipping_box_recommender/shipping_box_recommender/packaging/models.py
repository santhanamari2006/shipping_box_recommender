from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)

    length = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )

    width = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )

    height = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )

    weight = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )

    image = models.ImageField(
        upload_to="products/",
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    @property
    def total_amount(self):
        return sum(
            item.subtotal for item in self.items.all()
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product.name


class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)

    length = models.DecimalField(max_digits=8, decimal_places=2)
    width = models.DecimalField(max_digits=8, decimal_places=2)
    height = models.DecimalField(max_digits=8, decimal_places=2)

    max_weight = models.DecimalField(max_digits=8, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
