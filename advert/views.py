from datetime import datetime, timedelta
from django.db.models import Avg, Count, Sum
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from advert.exceptions import (
    OnlyOrdererCanCommentError,
    ProductOwnerCannotCommentError,
    UserMustHasDeliveryAddressError,
)
from advert.filter import OrderFilter, ProductFilter, SellerDeliveryFilter
from advert.serializers import (
    AddProductCommentSerializer,
    AddProductImageSerializer,
    ProductCreateSerializer,
    ProductFavoriteSerializer,
    ProductImageSerializer,
    ProductOrderCreateSerializer,
    ProductOrderSerializer,
    SellerDeliveryCreateSerializer,
    SellerDeliveryDetailSerializer,
    UpdateProductOrderStatusSerializer,
    ProductCommentSerializer,
    ProductsSectionSerializer,
    ProductsSectionCreateSerializer,
    ProductEssentialSerializer,
    UpdateProductQuantitySerializer,
)
from authentication.models import User
from core.exceptions import NotAuthorized
from core.permissions import (
    AllowOnlyVendor,
    AllowOnlyVendorOnDetroyAndCreate,
    AllowUserOnlyOnGet,
)
from .models import (
    ProductFavorite,
    ProductOrder,
    Product,
    ProductStatus,
    ProductType,
    ProductsSection,
    SellerDelivery,
    OrderStatus,
)
from .use_cases.update_product_order_status import UpdateProductOrderStatusUseCase


class ProductsSectionView(ModelViewSet):
    queryset = ProductsSection.objects.all()
    serializer_class = ProductsSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductsSectionCreateSerializer
        return ProductsSectionSerializer

    def get_queryset(self):
        sections = ProductsSection.objects.all()

        for section in sections:
            products = Product.objects.all()

            if section.product_type == ProductType.MOST_SELLING_PRODUCTS.value:
                products = products.order_by("-product_order_product__count")
            elif section.product_type == ProductType.NEW_ADDED_PRODUCTS.value:
                products = products.order_by("-created_at")

            if section.categories.exists():
                products = products.filter(category__in=section.categories.all())[:10]

            section.products = products

        return sections

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


@extend_schema(
    responses={
        201: "",
    },
    request=ProductCreateSerializer,
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductEssentialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AllowOnlyVendorOnDetroyAndCreate]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    @extend_schema(
        responses={
            201: "",
        },
        request=ProductCreateSerializer,
        summary="Create product",
    )
    # def perform_create(self, serializer):
    #     serializer.save(seller=self.request.user)

    def create(self, request, *args, **kwargs):
        # Change serializer response data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        product = serializer.save(seller=user)
        product_serializer = ProductEssentialSerializer(product)
        return Response(product_serializer.data, status=201)

    def get_queryset(self):
        products = Product.objects.filter(status=ProductStatus.PUBLISHED.value)
        products.annotate(average_rating=Avg("product_comment_product__rating"))
        return products

    def perform_destroy(self, instance):
        if instance.seller != self.request.user:
            raise NotAuthorized()
        return super().perform_destroy(instance)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductCreateSerializer
        return ProductEssentialSerializer


    @extend_schema(
        responses={
            201: "",
        },
        request="",
        summary="Archive product",
    )
    @action(
        detail=True,
        methods=["PUT"],
        permission_classes=[AllowOnlyVendor],
        url_path="archive",
    )
    def archive(self, request, pk=None):
        product: Product = self.get_object()
        Product.objects.filter(id=product.id).update(
            status=ProductStatus.ARCHIVED.value
        )
        return Response(status=200)

    @extend_schema(
        responses={
            201: "",
        },
        request=UpdateProductQuantitySerializer,
        summary="Update product quantity",
    )
    @action(
        detail=True,
        methods=["PUT"],
        permission_classes=[IsAuthenticated],
        url_path="update-quantity",
    )
    def update_quantity(self, request, pk=None):
        product: Product = self.get_object()
        serializer = UpdateProductQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        product.update_quantity(quantity)
        return Response(status=201)

    @extend_schema(
        responses={
            200: "",
        },
        request=AddProductImageSerializer,
        summary="Add product image",
    )
    @action(
        detail=True,
        methods=["PUT"],
        url_path="add-images",
        permission_classes=[IsAuthenticated],
    )
    def add_images(self, request, pk=None):
        serializer = AddProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_image = serializer.save()
        product = self.get_object()
        product.images.add(product_image)
        return Response(status=201)

    @extend_schema(
        responses={
            201: "",
        },
        request=AddProductCommentSerializer,
        summary="Add product comment",
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="add-comment",
        permission_classes=[IsAuthenticated],
    )
    def add_comment(self, request, pk=None):
        product: Product = self.get_object()
        user = self.request.user
        serializer = AddProductCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data["comment"]
        rating = serializer.validated_data["rating"]

        # Vérifier si le propriétaire du produit ne peut pas commenter
        if product.is_product_seller(user):
            raise ProductOwnerCannotCommentError()

        # Vérifier si l'utilisateur à le droit de commenter le produit
        product.add_comment(user=user, comment=comment, rating=rating)

        # Autoriser uniquement les utilisateurs qui ont déjà commandé le produit
        if not product.can_add_comment(user):
            raise OnlyOrdererCanCommentError()

        return Response(status=201)

    @extend_schema(
        summary="Add product to favorite",
        request={},
        responses={
            201: "",
        },
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="add-favorite",
        permission_classes=[IsAuthenticated],
    )
    def add_favorite(self, request, pk=None):
        user = self.request.user
        product: Product = self.get_object()
        product.add_to_favorite(user)
        return Response(status=201)

    @extend_schema(
        responses={
            201: ProductCommentSerializer,
        },
        request="",
        summary="Get product comments",
    )
    @action(
        detail=True,
        methods=["GET"],
        url_path="comments",
        permission_classes=[IsAuthenticated],
    )
    def get_comments(self, request, pk=None):
        product: Product = self.get_object()
        comments = product.get_all_comments()
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses={
            201: ProductImageSerializer,
        },
        request="",
        summary="Get product images",
    )
    @action(detail=True, methods=["GET"], url_path="images")
    def get_images(self, request, pk=None):
        product: Product = self.get_object()
        images = product.get_images()
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses={
            201: "",
        },
        request=ProductOrderCreateSerializer,
        summary="Make order",
    )
    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="make-order",
    )
    def make_order(self, request, pk=None):
        product: Product = self.get_object()
        user = self.request.user

        if not user.has_delivery_address():
            raise UserMustHasDeliveryAddressError()

        serializer = ProductOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]
        delivery_method: SellerDelivery = serializer.validated_data["delivery_method"]
        payment_method = serializer.validated_data["payment_method"]

        product.make_order(
            user=user,
            quantity=quantity,
            delivery_method=delivery_method,
            payment_method=payment_method,
        )
        # Send notification to seller
        return Response(status=201)


class VendorProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductEssentialSerializer
    permission_classes = [AllowOnlyVendor]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(seller=user)


class ProductOrderListView(ListAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        products = ProductOrder.objects.all()
        if self.request.user.is_vendor():
            products = ProductOrder.objects.filter(store__user=self.request.user)
        else:
            products = ProductOrder.objects.filter(user=self.request.user)
        return products


class ProductOrderUpdateStatusView(UpdateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = UpdateProductOrderStatusSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        product_order: ProductOrder = self.get_object()
        status = serializer.validated_data["status"]
        update_product_order_use_case = UpdateProductOrderStatusUseCase(
            product_order=product_order, status=status, user=self.request.user
        )
        update_product_order_use_case.execute()
        ProductOrder.objects.filter(id=product_order.id).update(status=status)

    def partial_update(self, request, *args, **kwargs):
        order: ProductOrder = self.get_object()
        serializer = UpdateProductOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data["status"]
        update_product_order_use_case = UpdateProductOrderStatusUseCase(
            product_order=order, status=status, user=self.request.user
        )
        update_product_order_use_case.execute()
        ProductOrder.objects.filter(id=order.id).update(status=status)
        return Response(status=200)


class ProductFavoritesListView(ListAPIView):
    queryset = ProductFavorite.objects.all()
    serializer_class = ProductFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductFavorite.objects.filter(user=user)


class SellerStatisticsAPIView(APIView):
    def get(self, request):
        user = request.user  # L'utilisateur authentifié

        # Calculez les statistiques pour l'utilisateur connecté
        totat_orders = ProductOrder.objects.filter(store__user=user).aggregate(
            total_orders=Count("id"),
        )

        total_products_sold = ProductOrder.objects.filter(
            store__user=user, status=OrderStatus.DELIVERED.value
        ).aggregate(total_products_sold=Sum("quantity"))

        total_product = Product.objects.filter(store__user=user).aggregate(
            total_product=Count("id")
        )

        low_stock_products = Product.objects.filter(
            quantity__lt=10, store__user=user
        ).count()

        # Ajoutez la statistique des produits avec un stock faible
        seller_statistics = {
            "total_orders": totat_orders["total_orders"] or 0,
            "total_products_sold": total_products_sold["total_products_sold"] or 0,
            "total_products": total_product["total_product"] or 0,
            "low_stock_products": low_stock_products or 0,
        }

        return Response(data=seller_statistics)


class WeeklySalesAPIView(APIView):
    def get(self, request):
        user = request.user  # L'utilisateur authentifié

        # Calculez la date de début et de fin de la semaine courante
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Générez toutes les dates de la semaine courante
        date_range = [start_of_week + timedelta(days=i) for i in range(7)]

        # Récupérez les ventes par jour de la semaine courante
        daily_sales = (
            ProductOrder.objects.filter(
                store__user=user,
                delivery_date__range=(start_of_week, end_of_week),
                status=OrderStatus.DELIVERED.value,
            )
            .values("delivery_date")
            .annotate(total_sales=Sum("total_price"))
        )

        # Créez une liste d'objets avec les clés "amount" et "date"
        sales_by_day = [
            {"amount": entry["total_sales"] or 0, "date": str(entry["delivery_date"])}
            for entry in daily_sales
        ]

        # Remplissez les dates sans vente avec un montant de 0
        for date in date_range:
            if not any(d["date"] == str(date) for d in sales_by_day):
                sales_by_day.append({"amount": 0, "date": str(date)})

        return Response(sales_by_day)


class SellerDeliveryView(ModelViewSet):
    queryset = SellerDelivery.objects.all()
    serializer_class = SellerDeliveryCreateSerializer
    permission_classes = [IsAuthenticated, AllowUserOnlyOnGet]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SellerDeliveryFilter

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SellerDeliveryCreateSerializer
        return SellerDeliveryDetailSerializer

    def get_queryset(self):
        user: User = self.request.user
        seller_delivery = SellerDelivery.objects.all()
        if user.is_vendor():
            return SellerDelivery.objects.filter(store__user=user)
        return seller_delivery
