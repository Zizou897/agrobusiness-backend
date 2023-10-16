from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'category' , 'created_at')
    ordering = ('-created_at',)