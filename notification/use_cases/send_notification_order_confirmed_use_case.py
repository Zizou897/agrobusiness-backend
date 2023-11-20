from advert.models import ProductOrder


class SendNotificationOrderConfirmedUseCase:
    def __init__(self, order_id):
        self.order_id = order_id

    def execute(self):
        order = ProductOrder.objects.get(id=self.order_id)

