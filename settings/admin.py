from django.contrib import admin
from .models import ProductCategory, Sectors, Measure, PaymentMethod


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Sectors)
class SectorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_name', 'created_at']
    search_fields = ['name', 'short_name']
    list_filter = ['created_at']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
