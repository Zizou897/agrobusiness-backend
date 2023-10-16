from rest_framework import serializers
from advert.models import Product, ProductCart, ProductComment, ProductFavorite, ProductImage, ProductOrder, SellerDelivery


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "quantity",
            "category",
            "manufacturer",
            "made_in",
            "measure",
            "stock_status",
            "user",
            "entreprise",
            "image",
            "created_at",
        ]


class ProductEssentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "category",
            "manufacturer",
            "made_in",
            "measure",
            "stock_status",
            "user",
            "entreprise",
            "image",
            "created_at",
        ]


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class AddProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "image",
            "product",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'



class AddProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = [
            "comment",
            "product",
            "user",
        ]


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'



class AddProductToFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFavorite
        fields = [
            "user",
            "product",
        ]


class ProductFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFavorite
        fields = '__all__'


class ProductOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            "product",
            "user",
            "quantity",
            "unit_price",
            "payment_method",
            "status",
            "created_at",
        ]



class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'



class UpdateProductOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            "status",
        ]


class AddProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = [
            "user",
            "product",
            "quantity",
        ]


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = '__all__'



class SellerDeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDelivery
        fields = [
            "user",
            "product",
            "delivery_method",
            "delivery_time"
        ]


class SellerDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDelivery
        fields = '__all__'