from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


def generate_unique_slug(instance, value):
    base = slugify(value) or 'item'
    slug, n = base, 2
    qs = type(instance).objects.exclude(pk=instance.pk)
    while qs.filter(slug=slug).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # noqa: RUF012
        indexes = [  # noqa: RUF012
            models.Index(fields=['name']),
            models.Index(fields=['is_active', 'category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name