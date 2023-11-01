from django.contrib import admin
from .models import Product, SellerDelivery, ProductImage, ProductsSection, ProductOrder


# Register your models here.
@admin.register(Product)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "quantity", "status", "category", "created_at")
    ordering = ("-created_at",)


@admin.register(SellerDelivery)
class SellerDeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "delivery_time", "delivery_price", "created_at")
    ordering = ("-created_at",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("is_main", "image", "created_at")
    ordering = ("-created_at",)


@admin.register(ProductsSection)
class SectionProduitsAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    ordering = ("-created_at",)


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "user",
        # "store",
        "product",
        "quantity",
        "total_price",
        "created_at",
    )
    ordering = ("-created_at",)
