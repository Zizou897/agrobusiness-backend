from rest_framework.viewsets import ModelViewSet
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
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView
from core.exceptions import NotAuthorized
from .models import ProductFavorite, ProductOrder, Product
from django_filters import rest_framework as filters


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data["seller"] = user
        return super().perform_create(serializer)

    # Si l'utilisateur est un vendeur, il ne peut voir que ses produits
    # def get_queryset(self):
    #     return Product.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductCreateSerializer
        return ProductDetailsSerializer

    @action(detail=True, methods=["PUT"])
    def update_quantity(self, request, pk=None):
        product = self.get_object()
        product.update_quantity(request.data.get("quantity"))
        return Response(status=201)

    @action(detail=True, methods=["PUT"], url_path="add-images")
    def add_images(self, request, pk=None):
        serializer = AddProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_image = serializer.save()
        product = self.get_object()
        product.images.add(product_image)
        return Response(status=201)

    @action(detail=True, methods=["POST"], url_path="add-comment")
    def add_comment(self, request, pk=None):
        product: Product = self.get_object()
        user = self.request.user
        serializer = AddProductCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data["comment"]
        product.add_comment(user, comment)
        return Response(status=201)

    @action(detail=True, methods=["POST"], url_path="add-favorite")
    def add_favorite(self, request, pk=None):
        user = self.request.user
        product: Product = self.get_object()
        product.add_to_favorite(user)
        return Response(status=201)

    @action(detail=True, methods=["GET"], url_path="comments")
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

    @action(detail=True, methods=["POST"])
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
        return ProductOrder.objects.filter(user=self.request.user)


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
