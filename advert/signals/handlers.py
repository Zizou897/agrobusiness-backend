from django.dispatch import receiver
from notification.signals import order_delivered
from advert.use_cases.update_product_quantity_use_case import (
    UpdateProductQuantityUseCase,
)


@receiver(order_delivered)
def update_product_quantity(sender, **kwargs):
    order_id = kwargs["order_id"]
    use_case = UpdateProductQuantityUseCase(order_id)
    use_case.execute()
