from rest_framework import serializers
from cities_light.models import Country
from settings.models import (
    DeliveryMethod,
    Measure,
    PaymentMethod,
    ProductCategory,
    Sectors,
)


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["name", "language_key"]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "language_key", "slug", "image"]


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = ["id", "name", "language_key"]


class SectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = ["name", "language_key"]


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ["id", "name", "short_name", "language_key"]


class MeasureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ["name", "short_name", "language_key"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "name",
            "logo",
            "language_key",
        ]


class PaymentMethodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "name",
        ]


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = [
            "id",
            "name",
            "language_key",
        ]


class DeliveryMethodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ["name", "language_key"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'slug']