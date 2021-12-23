
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return f"Catégorie {self.pk}: {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=254, unique=True)
    nutriscore = models.CharField(max_length=1)
    nutrients = models.JSONField(default=dict)
    brand = models.CharField(max_length=254, null=True)
    description = models.TextField(null=True)
    store = models.CharField(max_length=254, null=True)
    picture = models.URLField(max_length=300, null=True)
    url = models.URLField(max_length=300)
    # Foreign Key(s):
    categories = models.ManyToManyField(Category, related_name="products")

    def __str__(self):
        return f"Produit {self.pk}: {self.name} / Nutriscore: {self.nutriscore} / Marque(s): {self.brand} / Url: {self.url}"


class Favorite(models.Model):
    # Foreign Key(s):
    substitute = models.ForeignKey(
        Product,
        related_name="favorites_as_substitute",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name="favorites_as_product",
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('substitute', 'product', 'profile')

    def __str__(self):
        return f"Favori {self.pk}: Substitut: {self.substitute} / Produit substitué: {self.product} / {self.profile}"
