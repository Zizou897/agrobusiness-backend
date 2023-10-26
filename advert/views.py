from rest_framework.viewsets import ModelViewSet
from advert.exceptions import (
    OnlyOrdererCanCommentError,
    OnlyOwnerOfCartCanDeleteError,
    ProductOwnerCannotCommentError,
)
from advert.filter import ProductFilter
from advert.serializers import (
    AddProductCommentSerializer,
    AddProductImageSerializer,
    ProductCreateSerializer,
    ProductDetailsSerializer,
    ProductFavoriteSerializer,
    ProductImageSerializer,
    ProductOrderCreateSerializer,
    ProductOrderSerializer,
    UpdateProductOrderStatusSerializer,
    ProductCommentSerializer,
    ProductsSectionSerializer,
    ProductsSectionCreateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView
from authentication.models import ProfilTypeEnums
from core.exceptions import NotAuthorized
from .models import (
    ProductFavorite,
    ProductOrder,
    Product,
    ProductType,
    ProductsSection,
    ProductCart,
)
from django_filters import rest_framework as filters
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        products = Product.objects.annotate(
            average_rating=Avg("product_comment_product__rating")
        )
        user_profil = self.request.user.profil_type

        if user_profil in [
            ProfilTypeEnums.AGRIPRENEUR.value,
            ProfilTypeEnums.MERCHANT.value,
        ]:
            return products.filter(seller=self.request.user)

        return products

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductCreateSerializer
        return ProductDetailsSerializer

    @action(detail=True, methods=["PUT"], permission_classes=[IsAuthenticated])
    def update_quantity(self, request, pk=None):
        product = self.get_object()
        product.update_quantity(request.data.get("quantity"))
        return Response(status=201)

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

    @action(
        detail=True,
        methods=["POST"],
        url_path="add-cart",
        permission_classes=[IsAuthenticated],
    )
    def add_cart(self, request, pk=None):
        user = self.request.user
        product: Product = self.get_object()
        product.add_to_cart(user)
        return Response(status=201)

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

    @action(detail=True, methods=["GET"])
    def get_images(self, request, pk=None):
        product: Product = self.get_object()
        images = product.get_images()
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def make_order(self, request, pk=None):
        product: Product = self.get_object()
        user = self.request.user
        serializer = ProductOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        seller_delivery = serializer.validated_data["seller_delivery"]
        payment_method = serializer.validated_data["payment_method"]
        order = product.make_order(
            user=user,
            quantity=quantity,
            seller_delivery=seller_delivery,
            payment_method=payment_method,
        )
        # Send notification to seller
        return Response(status=201)


class ProductOrderListView(ListAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        products = ProductOrder.objects.filter(user=self.request.user)
        return products


class ProductOrderUpdateStatusView(UpdateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = UpdateProductOrderStatusSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        # Update order status
        order: ProductOrder = self.get_object()
        serializer = UpdateProductOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify if the user is the seller of the product
        if order.product.user != request.user:
            raise NotAuthorized()

        order.status = serializer.validated_data["status"]
        order.save(update_fields=["status"])


class ProductFavoritesListView(ListAPIView):
    queryset = ProductFavorite.objects.all()
    serializer_class = ProductFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductFavorite.objects.filter(user=user)


class ProductCartListView(ListAPIView):
    queryset = ProductFavorite.objects.all()
    serializer_class = ProductFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductFavorite.objects.filter(user=user)


class ProductCartDeleteView(UpdateAPIView):
    queryset = ProductCart.objects.all()
    serializer_class = ProductFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        # Update order status
        product_cart: ProductCart = self.get_object()

        # Verify if the user is the owner of the favorite
        if product_cart.user != request.user:
            raise OnlyOwnerOfCartCanDeleteError()

        product_cart.delete()
