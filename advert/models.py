import uuid
from cities_light.models import Country
from django.db import models
from authentication.models import User
from core.base_enum import ExtendedEnum
from core.constants import PRODUCT_IMAGE_PATH
from core.validators import validate_image_extension, validate_image_size
from settings.models import PaymentMethod


class ProductStatus(ExtendedEnum):
    PUBLISH = "PUBLISH"
    UNPUBLISH = "UNPUBLISH"
    WAIT = "WAIT"
    REFUSED = "REFUSED"


class StockStatus(ExtendedEnum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class OrderStatus(ExtendedEnum):
    RECEIVED = "RECEIVED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"
    RETURNED = "RETURNED"


class SellerDelivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name="Seller delivery product",
        related_name="seller_delivery_product",
    )
    delivery_method = models.ForeignKey(
        "settings.DeliveryMethod",
        on_delete=models.CASCADE,
        verbose_name="Seller delivery delivery method",
        related_name="seller_delivery_method",
    )
    delivery_time = models.PositiveIntegerField(
        verbose_name="Seller delivery delivery time in days"
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="Seller delivery user",
        related_name="seller_delivery_user",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Seller delivery created at"
    )

    class Meta:
        verbose_name = "Seller delivery"
        verbose_name_plural = "Seller deliveries"


class Product(models.Model):
    STATUS = (
        (ProductStatus.PUBLISH.value, "Publié"),
        (ProductStatus.UNPUBLISH.value, "Non publié"),
        (ProductStatus.WAIT.value, "En attente"),
        (ProductStatus.REFUSED.value, "Refusé"),
    )

    STOCK_STATUS = (
        (StockStatus.IN_STOCK.value, "En stock"),
        (StockStatus.OUT_OF_STOCK.value, "En rupture de stock"),
    )
    images = models.ManyToManyField(
        "advert.ProductImage",
        verbose_name="Product images",
        related_name="product_images",
        blank=True,
    )
    name = models.CharField(max_length=255, verbose_name="Product name")
    description = models.TextField(verbose_name="Product description")
    price = models.FloatField(verbose_name="Product price")
    quantity = models.PositiveIntegerField(verbose_name="Product quantity", default=0)
    category = models.ForeignKey(
        "settings.ProductCategory",
        on_delete=models.CASCADE,
        verbose_name="Product product category",
        related_name="product_category",
    )
    made_in = models.ForeignKey(
        Country,
        max_length=255,
        verbose_name="Product made in",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    measure = models.ForeignKey(
        "settings.Measure", on_delete=models.CASCADE, verbose_name="Product measure"
    )
    status = models.CharField(
        choices=STATUS,
        max_length=255,
        verbose_name="Product status",
        default=ProductStatus.WAIT.value,
    )
    stock_status = models.CharField(
        choices=STOCK_STATUS,
        max_length=255,
        verbose_name="Product stock status",
        default=StockStatus.IN_STOCK.value,
    )
    seller = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="Product seller user",
        related_name="product_seller_user",
    )
    entreprise = models.ForeignKey(
        "account.Entreprise",
        on_delete=models.CASCADE,
        verbose_name="Product seller entreprise",
        related_name="product_seller_entreprise",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product created at"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def add_to_favorite(self, user: User):
        ProductFavorite.objects.create(product=self, user=user)

    def remove_from_favorite(self, user: User):
        ProductFavorite.objects.filter(product=self, user=user).delete()

    def add_comment(self, user: User, comment: str):
        ProductComment.objects.create(product=self, user=user, comment=comment)

    def get_all_comments(self):
        return ProductComment.objects.filter(product=self)

    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def make_order(self, **kwargs):
        user = kwargs.get("user")
        quantity = kwargs.get("quantity")
        seller_delivery: SellerDelivery = kwargs.get("seller_delivery")
        payment_method: PaymentMethod = kwargs.get("payment_method")
        order = ProductOrder.objects.create(
            product=self,
            user=user,
            quantity=quantity,
            unit_price=self.price,
            total_price=self.price * quantity,
            payment_method=payment_method,
            delivery_method=seller_delivery.delivery_method,
            delivery_time=seller_delivery.delivery_time,
        )
        return order


class ProductImage(models.Model):
    is_main = models.BooleanField(default=False, verbose_name="Is main product image")
    image = models.ImageField(
        upload_to=PRODUCT_IMAGE_PATH,
        verbose_name="Product image",
        validators=[validate_image_size, validate_image_extension],
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product image created at"
    )

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"

    def __str__(self):
        return self.image.name

class ProductComment(models.Model):
    comment = models.TextField(verbose_name="Product comment")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product comment product",
        related_name="product_comment_product",
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="Product comment user",
        related_name="product_comment_user",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product comment created at"
    )

    class Meta:
        verbose_name = "Product comment"
        verbose_name_plural = "Product comments"


class ProductFavorite(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product favorite product",
        related_name="product_favorite_product",
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="Product favorite user",
        related_name="product_favorite_user",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product favorite created at"
    )

    class Meta:
        verbose_name = "Product favorite"
        verbose_name_plural = "Product favorites"


class ProductOrder(models.Model):
    STATUS = (
        (OrderStatus.RECEIVED.value, "Reçu"),
        (OrderStatus.PAYMENT_PENDING.value, "En attente de paiement"),
        (OrderStatus.OUT_FOR_DELIVERY.value, "En cours de livraison"),
        (OrderStatus.DELIVERED.value, "Livré"),
        (OrderStatus.CANCELED.value, "Annulé"),
        (OrderStatus.RETURNED.value, "Retourné"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(
        max_length=255, verbose_name="Product order reference", unique=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product order product",
        related_name="product_order_product",
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="Product order user",
        related_name="product_order_user",
    )
    quantity = models.PositiveIntegerField(verbose_name="Product order quantity")
    unit_price = models.FloatField(verbose_name="Product order unit price")
    total_price = models.FloatField(verbose_name="Product order price")
    payment_method = models.ForeignKey(
        "settings.PaymentMethod",
        on_delete=models.CASCADE,
        verbose_name="Product order payment method",
        related_name="product_order_payment_method",
    )
    delivery_method = models.ForeignKey(
        "SellerDelivery",
        on_delete=models.CASCADE,
        verbose_name="Product order delivery method",
        related_name="product_order_delivery_method",
    )
    status = models.CharField(
        choices=STATUS,
        max_length=255,
        verbose_name="Product order status",
        default=OrderStatus.RECEIVED.value,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product order created at"
    )

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"CMD-{self.created_at.strftime('%Y%m%d%H%M%S')}"
        super(ProductOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product order"
        verbose_name_plural = "Product orders"
