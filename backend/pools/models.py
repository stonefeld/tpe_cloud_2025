from django.db import models

from products.models import Product


class Pool(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pools")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    min_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Pool({self.product.name})"


class Request(models.Model):
    pool = models.ForeignKey(
        Pool,
        on_delete=models.CASCADE,
        related_name="requests",
    )
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("pool", "email")
