from advert.exceptions import StatusNotValidError
from advert.models import OrderStatus, ProductOrder
from authentication.models import ProfilTypeEnums, User
from core.exceptions import NotAuthorized


class UpdateProductOrderStatusUseCase:
    def __init__(self, **kwargs):
        self.product_order: ProductOrder = kwargs.get("product_order")
        self.status: str = kwargs.get("status")
        self.user: User = kwargs.get("user")

    def execute(self):
        status_is_allowed = self.status in [
            OrderStatus.CANCELED.value,
            OrderStatus.DELIVERED.value,
            OrderStatus.RECEIVED.value,
            OrderStatus.PENDING.value,
            OrderStatus.READY_TO_BE_DELIVERED.value,
        ]

        if not status_is_allowed:
            raise StatusNotValidError()

        locked_status = [
            OrderStatus.CANCELED.value,
            OrderStatus.DELIVERED.value,
        ]

        if self.product_order.status in locked_status:
            raise NotAuthorized()

        # Check if user has the right to update the order
        user_has_right = (
            self.product_order.user == self.user
            or self.product_order.product.seller == self.user
        )

        if not user_has_right:
            raise NotAuthorized()

        vendor_allowed_status = [
            OrderStatus.CANCELED.value,
            OrderStatus.DELIVERED.value,
            OrderStatus.RECEIVED.value,
            OrderStatus.READY_TO_BE_DELIVERED.value,
        ]

        client_allowed_status = [
            OrderStatus.CANCELED.value,
        ]

        if (
            self.user.profil_type
            in [ProfilTypeEnums.AGRIPRENEUR.value, ProfilTypeEnums.MERCHANT.value]
            and self.status not in vendor_allowed_status
        ):
            raise NotAuthorized()

        if (
            self.user.profil_type == ProfilTypeEnums.USER.value
            and self.status not in client_allowed_status
        ):
            raise NotAuthorized()
