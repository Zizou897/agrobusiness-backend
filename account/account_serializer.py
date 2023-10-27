from rest_framework import serializers

from account.models import Entreprise


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
            "web_site",
            "description",
        ]
