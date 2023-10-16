import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.base_enum import ExtendedEnum
from cities_light.models import Country
from django.core.validators import MinLengthValidator


class GenderEnums(ExtendedEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class ProfilTypeEnums(ExtendedEnum):
    ENTREPRISE = 'ENTREPRISE'
    FARMER = 'FARMER'
    MERCHANT = 'MERCHANT'
    USER = 'USER'


class User(AbstractUser):
    PROFIL_TYPE = (
        (ProfilTypeEnums.ENTREPRISE.value, 'Entreprise'),
        (ProfilTypeEnums.USER.value, 'Utilisateur'),
        (ProfilTypeEnums.FARMER.value, 'Agriculteur'),
        (ProfilTypeEnums.MERCHANT.value, 'Commerçant')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(
        default=False, verbose_name="Est vérifié ?")
    profil_type = models.CharField(choices=PROFIL_TYPE, max_length=255, verbose_name="Profil type",
                                   default=ProfilTypeEnums.USER.value)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email


class HOTPDevice(models.Model):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE, related_name='hotp')
    key = models.CharField(max_length=80, validators=[MinLengthValidator(40)],
                           help_text="A hex-encoded secret key of up to 40 bytes.", blank=True)
    counter = models.BigIntegerField(default=0,
                                     help_text="The counter value of the latest verified token. The next token must be at a higher counter value.",
                                     blank=True)
