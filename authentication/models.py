import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.base_enum import ExtendedEnum
from cities_light.models import Country
from django.core.validators import MinLengthValidator
from core.constants import USER_IMAGE_PATH
from core.validators import validate_image_extension, validate_image_size


class GenderEnums(ExtendedEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class ProfilTypeEnums(ExtendedEnum):
    AGRIPRENEUR = "AGRIPRENEUR"
    MERCHANT = "MERCHANT"
    USER = "USER"


class User(AbstractUser):
    PROFIL_TYPE = (
        (ProfilTypeEnums.USER.value, "Utilisateur"),
        (ProfilTypeEnums.AGRIPRENEUR.value, "Agripreneur"),
        (ProfilTypeEnums.MERCHANT.value, "Commerçant"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(
        upload_to=USER_IMAGE_PATH,
        verbose_name="Photo de profil",
        blank=True,
        null=True,
        validators=[validate_image_size, validate_image_extension],
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False, verbose_name="Est vérifié ?")
    profil_type = models.CharField(
        choices=PROFIL_TYPE,
        max_length=255,
        verbose_name="Profil type",
        default=ProfilTypeEnums.USER.value,
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def add_delivery_address(self, **kwargs):
        address = kwargs.get("address")
        city = kwargs.get("city")
        is_main = kwargs.get("is_main")

        if is_main:
            main_address = UserDeliveryAddress.objects.filter(
                user=self, is_main=True
            ).first()
            if main_address:
                main_address.is_main = False
                main_address.save(update_fields=["is_main"])

        return UserDeliveryAddress.objects.create(
            address=address,
            city=city,
            country=self.country,
            user=self,
            is_main=is_main,
        )
    
    def has_delivery_address(self):
        return UserDeliveryAddress.objects.filter(user=self).exists()

    def get_delivery_addresses(self):
        return UserDeliveryAddress.objects.filter(user=self)

    def get_main_delivery_address(self):
        return UserDeliveryAddress.objects.filter(user=self, is_main=True).first()

    def is_vendor(self):
        return self.profil_type in [
            ProfilTypeEnums.AGRIPRENEUR.value,
            ProfilTypeEnums.MERCHANT.value,
        ]

    def __str__(self):
        return self.email


class UserDeliveryAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="delivery_addresses"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.address} - {self.country}"


class HOTPDevice(models.Model):
    user = models.OneToOneField(
        "authentication.User", on_delete=models.CASCADE, related_name="hotp"
    )
    key = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(40)],
        help_text="A hex-encoded secret key of up to 40 bytes.",
        blank=True,
    )
    counter = models.BigIntegerField(
        default=0,
        help_text="The counter value of the latest verified token. The next token must be at a higher counter value.",
        blank=True,
    )


class BroadcastGroup(models.Model):
    PROFIL_TYPE = (
        (ProfilTypeEnums.USER.value, "Utilisateur"),
        (ProfilTypeEnums.AGRIPRENEUR.value, "Agripreneur"),
        (ProfilTypeEnums.MERCHANT.value, "Commerçant"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type_user = models.CharField(
        choices=PROFIL_TYPE,
        max_length=255,
        verbose_name="Profil type",
        default=ProfilTypeEnums.USER.value,
    )
    is_entreprise = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
