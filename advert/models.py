import uuid
from cities_light.models import Country
from django.db import models
from core.base_enum import ExtendedEnum


class ProductStatus(ExtendedEnum):
    PUBLISH = 'PUBLISH'
    UNPUBLISH = 'UNPUBLISH'
    WAIT = 'WAIT'
    REFUSED = 'REFUSED'


class StockStatus(ExtendedEnum):
    IN_STOCK = 'IN_STOCK'
    OUT_OF_STOCK = 'OUT_OF_STOCK'


class OrderStatus(ExtendedEnum):
    RECEIVED = 'RECEIVED'
    PAYMENT_PENDING = 'PAYMENT_PENDING'
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY'
    DELIVERED = 'DELIVERED'
    CANCELED = 'CANCELED'
    RETURNED = 'RETURNED'


class Product(models.Model):
    STATUS = (
        (ProductStatus.PUBLISH.value, 'Publié'),
        (ProductStatus.UNPUBLISH.value, 'Non publié'),
        (ProductStatus.WAIT.value, 'En attente'),
        (ProductStatus.REFUSED.value, 'Refusé'),
    )

    STOCK_STATUS = (
        (StockStatus.IN_STOCK.value, 'En stock'),
        (StockStatus.OUT_OF_STOCK.value, 'En rupture de stock'),
    )

    name = models.CharField(max_length=255, verbose_name="Product name")
    description = models.TextField(verbose_name="Product description")
    price = models.FloatField(verbose_name="Product price")
    quantity = models.PositiveIntegerField(
        verbose_name="Product quantity", default=0)
    category = models.ForeignKey('settings.ProductCategory', on_delete=models.CASCADE,
                                 verbose_name="Product product category", related_name="product_category")
    manufacturer = models.CharField(
        max_length=255, verbose_name="Product manufacturer", blank=True)
    made_in = models.ForeignKey(Country, max_length=255, verbose_name="Product made in",
                                null=True, blank=True, on_delete=models.CASCADE)
    measure = models.ForeignKey(
        'settings.Measure', on_delete=models.CASCADE, verbose_name="Product measure")
    status = models.CharField(choices=STATUS, max_length=255,
                              verbose_name="Product status", default=ProductStatus.WAIT.value)
    stock_status = models.CharField(choices=STOCK_STATUS, max_length=255,
                                    verbose_name="Product stock status", default=StockStatus.IN_STOCK.value)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="Product seller user",
                             related_name="product_seller_user")
    entreprise = models.ForeignKey('account.Entreprise', on_delete=models.CASCADE, verbose_name="Product seller entreprise",
                                   related_name="product_seller_entreprise", null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product created at")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='uploads/images/',
                              verbose_name="Product image")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product image product",
                                related_name="product_image_product")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product image created at")

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"


class ProductComment(models.Model):
    comment = models.TextField(verbose_name="Product comment")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product comment product",
                                related_name="product_comment_product")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="Product comment user",
                             related_name="product_comment_user")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product comment created at")

    class Meta:
        verbose_name = "Product comment"
        verbose_name_plural = "Product comments"


class ProductFavorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product favorite product",
                                related_name="product_favorite_product")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="Product favorite user",
                             related_name="product_favorite_user")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product favorite created at")

    class Meta:
        verbose_name = "Product favorite"
        verbose_name_plural = "Product favorites"


class ProductOrder(models.Model):
    STATUS = (
        (OrderStatus.RECEIVED.value, 'Reçu'),
        (OrderStatus.PAYMENT_PENDING.value, 'En attente de paiement'),
        (OrderStatus.OUT_FOR_DELIVERY.value, 'En cours de livraison'),
        (OrderStatus.DELIVERED.value, 'Livré'),
        (OrderStatus.CANCELED.value, 'Annulé'),
        (OrderStatus.RETURNED.value, 'Retourné'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(
        max_length=255, verbose_name="Product order reference", unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product order product",
                                related_name="product_order_product")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="Product order user",
                             related_name="product_order_user")
    quantity = models.PositiveIntegerField(
        verbose_name="Product order quantity")
    unit_price = models.FloatField(verbose_name="Product order unit price")
    total_price = models.FloatField(verbose_name="Product order price")
    payment_method = models.ForeignKey('settings.PaymentMethod', on_delete=models.CASCADE,
                                       verbose_name="Product order payment method", related_name="product_order_payment_method")
    delivery_method = models.ForeignKey('settings.DeliveryMethod', on_delete=models.CASCADE,
                                        verbose_name="Product order delivery method", related_name="product_order_delivery_method")
    delivery_time = models.PositiveIntegerField(
        verbose_name="Order delivery delivery time in days"
    )
    status = models.CharField(choices=STATUS, max_length=255,
                              verbose_name="Product order status", default=OrderStatus.RECEIVED.value)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product order created at")

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"CMD-{self.created_at.strftime('%Y%m%d%H%M%S')}"
        super(ProductOrder, self).save(*args, **kwargs)

    def get_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Product order"
        verbose_name_plural = "Product orders"


class ProductCart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="Cart user",
                             related_name="cart_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Cart product",
                                related_name="cart_product")
    quantity = models.PositiveIntegerField(verbose_name="Cart quantity")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Cart created at")

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return self.product.name

    def get_total(self):
        return self.product.price * self.quantity

    def update_quantity(self, quantity):
        self.quantity = quantity
        self.save(update_fields=['quantity'])

    def clear_cart(self):
        self.delete()


class SellerDelivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Seller delivery product",
                                related_name="seller_delivery_product")
    delivery_method = models.ForeignKey('settings.DeliveryMethod', on_delete=models.CASCADE,
                                        verbose_name="Seller delivery delivery method", related_name="seller_delivery_method")
    delivery_time = models.PositiveIntegerField(
        verbose_name="Seller delivery delivery time in days"
    )
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="Seller delivery user",
                             related_name="seller_delivery_user")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Seller delivery created at")

    class Meta:
        verbose_name = "Seller delivery"
        verbose_name_plural = "Seller deliveries"
