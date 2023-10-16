from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from settings.models import DeliveryMethod, Measure, PaymentMethod, ProductCategory, Sectors
from settings.serializers import DeliveryMethodCreateSerializer, DeliveryMethodSerializer, MeasureCreateSerializer, MeasureSerializer, PaymentMethodCreateSerializer, PaymentMethodSerializer, ProductCategoryCreateSerializer, ProductCategorySerializer, SectorCreateSerializer, SectorSerializer



class CategoryProductView(ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductCategoryCreateSerializer
        return ProductCategorySerializer
    

class SectorView(ModelViewSet):
    serializer_class = SectorSerializer
    queryset = Sectors.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SectorCreateSerializer
        return SectorSerializer
    

class MeasureView(ModelViewSet):
    serializer_class = MeasureSerializer
    queryset = Measure.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return MeasureCreateSerializer
        return MeasureSerializer
    

class PaymentMethodView(ModelViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer
    

class DeliveryMethodView(ModelViewSet):
    serializer_class = DeliveryMethodSerializer
    queryset = DeliveryMethod.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DeliveryMethodCreateSerializer
        return DeliveryMethodSerializer


    

