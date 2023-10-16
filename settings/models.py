from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product category name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Product category created at")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"


class Sectors(models.Model):
    name = models.CharField(max_length=255, verbose_name="Sector name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sector created at")

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"


class Measure(models.Model):
    name = models.CharField(max_length=255, verbose_name="Measure name")
    short_name = models.CharField(max_length=255, verbose_name="Measure short name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Measure created at")

    class Meta:
        verbose_name = "Measure"
        verbose_name_plural = "Measures"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Payment method name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Payment method created at")

    class Meta:
        verbose_name = "Payment method"
        verbose_name_plural = "Payment methods"


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Delivery method name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Delivery method created at")

    class Meta:
        verbose_name = "Delivery method"
        verbose_name_plural = "Delivery methods"