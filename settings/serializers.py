from rest_framework import serializers
from settings.models import DeliveryMethod, Measure, PaymentMethod, ProductCategory, Sectors


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'name',
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = '__all__'


class SectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = [
            'name',
        ]


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = '__all__'


class MeasureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = [
            'name',
            'short_name'
        ]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

    
class PaymentMethodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'name',
        ]


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = '__all__'



class DeliveryMethodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = [
            'name',
        ]