from rest_framework import serializers

from account.models import Entreprise, Store


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
            "name",
            "phone_number",
            "logo",
            "address",
            "description",
        ]