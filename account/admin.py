from django.contrib import admin
from .models import Entreprise, Store

# Register your models here.

# Change admin site title
admin.site.site_header = "Agri-jeune Administration"


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "created_at")
    ordering = ("-created_at",)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "created_at")
    ordering = ("-created_at",)
