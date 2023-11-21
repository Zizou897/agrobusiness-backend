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


class FCMDeviceSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    name = serializers.CharField(required=True)
    registration_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    type = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
