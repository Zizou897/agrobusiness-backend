from advert.exceptions import OrderQuantityCannotBeGreaterThanProductQuantityError
from advert.models import Product, ProductOrder, StockStatus


class UpdateProductQuantityUseCase:
    def __init__(self, order_id: str):
        self.order_id = order_id

    def execute(self):
        order = ProductOrder.objects.get(id=self.order_id)
        product: Product = order.product

        order_quantity_is_greater_than_product_quantity = (
            order.quantity > product.quantity
        )

        if order_quantity_is_greater_than_product_quantity:
            raise OrderQuantityCannotBeGreaterThanProductQuantityError()

        new_quantity = product.quantity - order.quantity
        product.update_quantity(new_quantity)
