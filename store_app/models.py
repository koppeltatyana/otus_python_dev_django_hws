from django.db import models


class Category(models.Model):
    """Модель Category"""

    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Product(models.Model):
    """Модель Product"""

    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)
