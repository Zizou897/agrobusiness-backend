from django.db import models
from core.constants import CATEGORY_IMAGE_PATH, PAYMENT_METHOD_IMAGE_PATH


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product category name")
    image = models.ImageField(
        upload_to=CATEGORY_IMAGE_PATH,
        verbose_name="Product category image",
        blank=True,
        null=True,
    )
    language_key = models.CharField(
        max_length=255,
        verbose_name="Product category language key",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product category created at"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"


class Sectors(models.Model):
    name = models.CharField(max_length=255, verbose_name="Sector name")
    language_key = models.CharField(
        max_length=255, verbose_name="Sectors language key", blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Sector created at"
    )

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"


class Measure(models.Model):
    name = models.CharField(max_length=255, verbose_name="Measure name")
    short_name = models.CharField(max_length=255, verbose_name="Measure short name")
    language_key = models.CharField(
        max_length=255, verbose_name="Measure language key", blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Measure created at"
    )

    class Meta:
        verbose_name = "Measure"
        verbose_name_plural = "Measures"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Payment method name")
    logo = models.ImageField(
        upload_to=PAYMENT_METHOD_IMAGE_PATH,
        verbose_name="Payment method logo",
        blank=True,
        null=True,
    )
    language_key = models.CharField(
        max_length=255, verbose_name="Payment method language key", null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Payment method created at"
    )

    class Meta:
        verbose_name = "Payment method"
        verbose_name_plural = "Payment methods"


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Delivery method name")
    language_key = models.CharField(
        max_length=255,
        verbose_name="Delivery method language key",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Delivery method created at"
    )

    class Meta:
        verbose_name = "Delivery method"
        verbose_name_plural = "Delivery methods"
