from django.contrib import admin
from .models import User, UserDeliveryAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "profil_type",
        "is_verified",
    ]
    search_fields = ["email"]


@admin.register(UserDeliveryAddress)
class UserDeliveryAddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "address",
        "city",
        "country",
        "is_main",
    ]
