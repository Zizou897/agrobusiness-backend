from django.contrib import admin
from .models import Entreprise

# Register your models here.

# Change admin site title
admin.site.site_header = "Agri-jeune Administration"

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "created_at")
    ordering = ("-created_at",)