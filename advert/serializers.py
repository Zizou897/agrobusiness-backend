from rest_framework import serializers
from account.serializers import StoreSerializer
from advert.models import (
    Product,
    ProductComment,
    ProductFavorite,
    ProductImage,
    ProductOrder,
    SellerDelivery,
    ProductsSection,
)
from authentication.serializers import (
    UserDeliveryAddressEssentialSerializer,
    UserEssentialSerializer,
)
from settings.serializers import (
    MeasureSerializer,
    PaymentMethodSerializer,
    ProductCategorySerializer,
)


class UpdateProductQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "quantity",
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
            "store",
            "measure",
            "stock_status",
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
    store = StoreSerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "short_description",
            "price",
            "quantity",
            "category",
            "made_in",
            "measure",
            "stock_status",
            "store",
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
    class Meta:
        model = ProductOrder
        fields = [
            "payment_method",
            "delivery_method",
            "quantity",
        ]


class UpdateProductOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            "status",
        ]


class SellerDeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDelivery
        fields = ["name", "delivery_time", "delivery_price"]


class SellerDeliveryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerDelivery
        fields = [
            "id",
            "name",
            "delivery_price",
            "delivery_time",
            "created_at",
        ]


class SellerDeliveryEssentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDelivery
        fields = [
            "id",
            "name",
            "delivery_price",
            "delivery_time",
        ]


class ProductOrderSerializer(serializers.ModelSerializer):
    product = ProductEssentialSerializer()
    user = UserEssentialSerializer()
    payment_method = PaymentMethodSerializer()
    store = StoreSerializer()
    delivery_address = UserDeliveryAddressEssentialSerializer()
    delivery_method = SellerDeliveryEssentialSerializer()

    class Meta:
        model = ProductOrder
        fields = "__all__"
