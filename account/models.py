import uuid
from django.db import models
from cities_light.models import Country

from core.constants import ENTERPRISE_IMAGE_PATH
from core.validators import validate_image_extension, validate_image_size


class Entreprise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="User entreprise",
        related_name="entreprise_user",
    )
    name = models.CharField(max_length=255, verbose_name="Nom de l'entreprise")
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name="Pays de l'entreprise",
        related_name="entreprise_country",
    )
    phone_number = models.CharField(
        max_length=255, verbose_name="Téléphone de l'entreprise"
    )
    logo = models.ImageField(
        upload_to=ENTERPRISE_IMAGE_PATH,
        verbose_name="Logo de l'entreprise",
        blank=True,
        null=True,
        validators=[
            validate_image_size,
            validate_image_extension
        ],
    )
    web_site = models.CharField(
        max_length=255, verbose_name="Site web de l'entreprise", blank=True, null=True
    )
    description = models.TextField(verbose_name="Description de l'entreprise")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création de l'entreprise"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification de l'entreprise"
    )

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="subscription_user",
    )
    is_active = models.BooleanField(
        default=False, verbose_name="User subscription is active"
    )
    subcription_date = models.DateTimeField(
        auto_now_add=True, verbose_name="User subscription date"
    )
    expiration_date = models.DateTimeField(
        verbose_name="User subscription expiration date"
    )
    subcription = models.ForeignKey(
        "account.Subscription",
        on_delete=models.CASCADE,
        verbose_name="User subcription",
        related_name="subscription_of_user",
    )
    payment_method = models.CharField(
        max_length=255, verbose_name="User subscription payment method"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="User subscription created at"
    )
    reference = models.CharField(
        max_length=255, verbose_name="User subscription reference"
    )

    def __str__(self):
        return self.user.email


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Subscription name")
    price = models.FloatField(verbose_name="Subscription price")
    duration = models.IntegerField(verbose_name="Subscription duration in days")
    offers = models.ManyToManyField("account.Offer", verbose_name="Subscription offers")

    def __str__(self):
        return self.name


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Offer name")
    description = models.TextField(verbose_name="Offer description")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Offer created at"
    )
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Offer modified at")

    def __str__(self):
        return self.name
