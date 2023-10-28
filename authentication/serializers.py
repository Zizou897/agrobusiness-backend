from fcm_django.models import FCMDevice
from rest_framework import serializers

from account.account_serializer import EntrepriseSerializer
from settings.serializers import CountrySerializer
from .models import ProfilTypeEnums, User, UserDeliveryAddress
from cities_light.models import Country


class VendorSerializer(serializers.ModelSerializer):
    entreprise = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "entreprise",
        ]

    def get_entreprise(self, obj):
        entreprise = obj.entreprise_user.first()
        if entreprise:
            return {
                "id": entreprise.id,
                "name": entreprise.name,
                "country": entreprise.country.name,
                "address": entreprise.address,
                "phone_number": entreprise.phone_number,
                "logo": entreprise.logo.url if entreprise.logo else None,
                "web_site": entreprise.web_site,
                "description": entreprise.description,
            }
        return None


class UserEssentialSerializer(serializers.ModelSerializer):
    entreprise = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "entreprise",
        ]

    def get_entreprise(self, obj):
        entreprise = obj.entreprise_user.first()
        if entreprise:
            return {
                "id": entreprise.id,
                "name": entreprise.name,
                "country": entreprise.country.name,
                "address": entreprise.address,
                "phone_number": entreprise.phone_number,
                "logo": entreprise.logo.url if entreprise.logo else None,
                "web_site": entreprise.web_site,
                "description": entreprise.description,
            }
        return None


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, write_only=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), required=False
    )
    phone_number = serializers.CharField(required=False, write_only=True)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    password2 = serializers.CharField(required=True, min_length=8, write_only=True)
    profil_type = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas"}
            )
        return attrs

    def create(self, validated_data):
        data = {
            "email": validated_data["email"],
            "username": validated_data["username"],
            "password": validated_data["password"],
            "country": validated_data["country"],
            "phone_number": validated_data["phone_number"],
            "first_name": validated_data["first_name"],
            "last_name": validated_data["last_name"],
            "profil_type": validated_data["profil_type"],
        }
        return User.objects.create_user(**data)

    def update(self, instance, validated_data):
        pass


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class EmailConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ResendOTPCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class FCMDeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = FCMDevice
        fields = ["name", "registration_id", "device_id", "type", "user"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "registration_id": instance.registration_id,
            "device_id": instance.device_id,
            "type": instance.type,
            "user": instance.user.id,
        }


class UserDeliveryAddressEssentialSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = UserDeliveryAddress
        fields = [
            "address",
            "city",
            "country",
            "is_main",
        ]


class UserDeliveryAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDeliveryAddress
        fields = [
            "address",
            "city",
            "is_main",
        ]
