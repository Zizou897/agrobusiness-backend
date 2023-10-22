from rest_framework import serializers
from advert.models import (
    Product,
    ProductComment,
    ProductFavorite,
    ProductImage,
    ProductOrder,
    SellerDelivery,
    SectionProduits
)
from authentication.serializers import UserEssentialSerializer
from settings.serializers import MeasureSerializer, ProductCategorySerializer


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "quantity",
            "category",
            "made_in",
            "measure",
            "stock_status",
            "entreprise",
            "seller"
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "image",
            "is_main",
        ]


class ProductEssentialSerializer(serializers.ModelSerializer):
    measure = MeasureSerializer()
    category = ProductCategorySerializer()
    made_in = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True)
    seller = UserEssentialSerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "category",
            "made_in",
            "measure",
            "stock_status",
            "seller",
            "entreprise",
            "images",
            "created_at",
        ]


class SectionProduitsSerializer(serializers.ModelSerializer):
    products = ProductEssentialSerializer(many=True, read_only=True)

    class Meta:
        model = SectionProduits
        fields = [
            "id",
            "name",
            "description",
            "categories",
            "product_type",
            "products",
        ]


class SectionProduitsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionProduits
        fields = [
            "name",
            "description",
            "categories",
            "product_type",
        ]


class ProductDetailsSerializer(serializers.ModelSerializer):
    measure = MeasureSerializer()
    category = ProductCategorySerializer()
    images = ProductImageSerializer(many=True)
    made_in = serializers.StringRelatedField()
    seller = UserEssentialSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class AddProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "is_main"]


class AddProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ["comment"]


class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserEssentialSerializer()
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductComment
        fields = "__all__"


class AddProductToFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFavorite
        fields = [
            "product",
        ]


class ProductFavoriteSerializer(serializers.ModelSerializer):
    product = ProductEssentialSerializer()

    class Meta:
        model = ProductFavorite
        fields = "__all__"


class ProductOrderCreateSerializer(serializers.ModelSerializer):
    seller_delivery = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=SellerDelivery.objects.all()
    )

    class Meta:
        model = ProductOrder
        fields = [
            "quantity",
            "unit_price",
            "payment_method",
            "seller_delivery",
            "status",
        ]


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = "__all__"


class UpdateProductOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            "status",
        ]


class SellerDeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDelivery
        fields = ["product", "delivery_method", "delivery_time"]


class SellerDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDelivery
        fields = "__all__"
