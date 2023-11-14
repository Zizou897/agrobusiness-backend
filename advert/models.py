import uuid
from cities_light.models import Country, City
from django.db import models
from advert.exceptions import OrderQuantityCannotBeGreaterThanProductQuantityError
from advert.utils import calculDeliveryDateByNumberOfDays
from authentication.models import User
from core.base_enum import ExtendedEnum
from core.constants import PRODUCT_IMAGE_PATH
from core.validators import validate_image_extension, validate_image_size
from settings.models import PaymentMethod
from django.db.models import Sum
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator


class ProductType(ExtendedEnum):
    ALL_PRODUCTS = "ALL_PRODUCTS"
    NEW_ADDED_PRODUCTS = "NEW_ADDED_PRODUCTS"
    MOST_SELLING_PRODUCTS = "MOST_SELLING_PRODUCTS"


class ProductStatus(ExtendedEnum):
    PUBLISH = "PUBLISH"
    UNPUBLISH = "UNPUBLISH"
    WAIT = "WAIT"
    REFUSED = "REFUSED"
    ARCHIVED = "ARCHIVED"


class StockStatus(ExtendedEnum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class OrderStatus(ExtendedEnum):
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    READY_TO_BE_DELIVERED = "READY_TO_BE_DELIVERED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class SellerDelivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, verbose_name="Seller delivery name", blank=True, null=True
    )
    delivery_time = models.PositiveIntegerField(
        verbose_name="Seller delivery delivery time in days"
    )
    delivery_price = models.IntegerField(
        verbose_name="Seller delivery delivery price",
        default=0,
    )
    store = models.ForeignKey(
        "account.Store",
        on_delete=models.CASCADE,
        verbose_name="Seller delivery user",
        related_name="seller_delivery_user",
        null=True,
        blank=True,
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
        (ProductStatus.ARCHIVED.value, "Archivé"),
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Product name")
    short_description = models.TextField(
        verbose_name="Product short description", blank=True, null=True
    )
    description = RichTextField(
        verbose_name="Product description",
        blank=True,
        null=True,
    )
    price = models.IntegerField(verbose_name="Product price")
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
        default=ProductStatus.PUBLISH.value,
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
    store = models.ForeignKey(
        "account.Store",
        on_delete=models.CASCADE,
        verbose_name="Product seller store",
        related_name="product_seller_store",
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

    def is_ordered_by(self, user: User):
        return ProductOrder.objects.filter(product=self, user=user).exists()

    def is_ordered(self):
        allow_status = [
            OrderStatus.PENDING.value,
            OrderStatus.RECEIVED.value,
            OrderStatus.READY_TO_BE_DELIVERED.value,
        ]
        return ProductOrder.objects.filter(
            product=self, status__in=allow_status
        ).exists()

    def can_be_archived(self):
        return not self.is_ordered()

    def is_product_seller(self, user: User):
        return self.seller == user

    def add_to_favorite(self, user: User):
        ProductFavorite.objects.create(product=self, user=user)

    def remove_from_favorite(self, user: User):
        ProductFavorite.objects.filter(product=self, user=user).delete()

    def add_comment(self, **kwargs):
        user = kwargs.get("user")
        comment = kwargs.get("comment")
        rating = kwargs.get("rating")
        ProductComment.objects.create(
            product=self, user=user, comment=comment, rating=rating
        )

    def can_add_comment(self, user: User):
        return ProductOrder.objects.filter(product=self, user=user).exists()

    def get_all_comments(self):
        return ProductComment.objects.filter(product=self)

    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def update_quantity(self, quantity):
        self.quantity = quantity
        self.save(update_fields=["quantity"])

    def make_order(self, **kwargs):
        user: User = kwargs.get("user")
        quantity = kwargs.get("quantity")
        delivery_method: SellerDelivery = kwargs.get("delivery_method")
        payment_method: PaymentMethod = kwargs.get("payment_method")
        order = ProductOrder.objects.create(
            product=self,
            user=user,
            delivery_address=user.get_main_delivery_address(),
            quantity=quantity,
            store=self.store,
            unit_price=self.price,
            total_price=self.price * quantity,
            payment_method=payment_method,
            delivery_method=delivery_method,
            delivery_date=calculDeliveryDateByNumberOfDays(
                delivery_method.delivery_time
            ),
        )
        # Update product quantity
        self.update_quantity(self.quantity - quantity)

        if self.quantity == 0:
            self.stock_status = StockStatus.OUT_OF_STOCK.value
            self.save(update_fields=["stock_status"])

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
    rating = models.PositiveIntegerField(
        verbose_name="Product comment rating",
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
    )
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
        (OrderStatus.PENDING.value, "En attente"),
        (OrderStatus.RECEIVED.value, "Reçu"),
        (OrderStatus.DELIVERED.value, "Livré"),
        (OrderStatus.CANCELED.value, "Annulé"),
        (OrderStatus.READY_TO_BE_DELIVERED.value, "Prêt à être livré"),
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
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="Product order user",
        related_name="product_order_user",
    )
    store = models.ForeignKey(
        "account.Store",
        on_delete=models.CASCADE,
        verbose_name="Product order store",
        related_name="product_order_store",
        null=True,
        blank=True,
    )
    delivery_method = models.ForeignKey(
        SellerDelivery,
        on_delete=models.CASCADE,
        verbose_name="Product order delivery method",
        related_name="product_order_delivery_method",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Product order item quantity", default=0
    )
    unit_price = models.IntegerField(
        verbose_name="Product order item unit price", default=0
    )
    total_price = models.IntegerField(
        verbose_name="Product order item total price", default=0
    )
    payment_method = models.ForeignKey(
        "settings.PaymentMethod",
        on_delete=models.CASCADE,
        verbose_name="Product order payment method",
        related_name="product_order_payment_method",
    )
    delivery_date = models.DateField(
        verbose_name="Product order delivery date", null=True, blank=True
    )
    delivery_address = models.ForeignKey(
        "authentication.UserDeliveryAddress",
        on_delete=models.CASCADE,
        verbose_name="Product order delivery address",
        related_name="product_order_delivery_address",
        blank=True,
        null=True,
    )
    status = models.CharField(
        choices=STATUS,
        max_length=255,
        verbose_name="Product order status",
        default=OrderStatus.PENDING.value,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Product order created at"
    )

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"PO-{uuid.uuid4().hex[:6].upper()}"

        # Check if is a new order
        is_new_order = not self.pk

        # Check if the quantity ordered is greater than the quantity of the product
        if self.quantity > self.product.quantity:
            raise OrderQuantityCannotBeGreaterThanProductQuantityError()

        # Calculate the total price of the order
        self.total_price = self.unit_price * self.quantity

        super(ProductOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product order"
        verbose_name_plural = "Product orders"


class ProductsSection(models.Model):
    PRODUCT_TYPE = (
        (ProductType.ALL_PRODUCTS.value, "Tous les produits"),
        (ProductType.NEW_ADDED_PRODUCTS.value, "Nouveaux produits ajoutés"),
        # (ProductType.MOST_SELLING_PRODUCTS.value, "Produits les plus vendus"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nom de la section")
    description = models.TextField(verbose_name="Description de la section")
    categories = models.ManyToManyField(
        "settings.ProductCategory",
        verbose_name="Product product category",
        related_name="product_category_section",
        blank=True,
    )
    product_type = models.CharField(
        choices=PRODUCT_TYPE,
        max_length=255,
        verbose_name="Product type",
        default=ProductType.ALL_PRODUCTS.value,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Section created at"
    )

    def __str__(self):
        return self.name
