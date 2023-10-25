from rest_framework import serializers
from advert.models import (
    Product,
    ProductComment,
    ProductFavorite,
    ProductImage,
    ProductOrder,
    SellerDelivery,
    ProductsSection,
    ProductCart
)
from authentication.serializers import UserEssentialSerializer
from settings.serializers import MeasureSerializer, ProductCategorySerializer


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = "__all__"


class ProductCartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = [
            "product",
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "short_description",
            "description",
            "price",
            "quantity",
            "category",
            "made_in",
            "measure",
            "stock_status",
            "entreprise",
            # "seller"
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


class ProductsSectionSerializer(serializers.ModelSerializer):
    products = ProductEssentialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductsSection
        fields = [
            "id",
            "name",
            "description",
            "categories",
            "product_type",
            "products",
        ]


class ProductsSectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsSection
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
        fields = ["comment", "rating"]


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
