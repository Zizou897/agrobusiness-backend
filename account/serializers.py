from rest_framework import serializers
from fcm_django.models import FCMDevice
from account.models import Entreprise, Store
from authentication.models import User


class EntrepriseSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = Entreprise
        fields = [
            "id",
            "name",
            "phone_number",
            "logo",
            "country",
            "address",
            "description",
        ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "phone_number",
            "logo",
            "address",
            "description",
        ]


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "user",
            "name",
            "phone_number",
            "logo",
            "address",
            "description",
        ]


class FCMDeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = FCMDevice
        fields = ["name", "registration_id", "device_id", "type", "user"]
