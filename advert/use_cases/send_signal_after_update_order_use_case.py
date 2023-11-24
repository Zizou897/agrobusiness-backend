from advert.models import OrderStatus, ProductOrder


class SendSignalAfterUpdateOrderUseCase:
    def __init__(self, status: str, order: ProductOrder):
        self.status = status
        self.order = order

    def execute(self):
        switcher = {
            OrderStatus.RECEIVED.value: lambda: self.order.send_signal_confirmed(),
            OrderStatus.READY_TO_BE_DELIVERED.value: lambda: self.order.send_signal_ready_to_deliver(),
            OrderStatus.DELIVERED.value: lambda: self.order.send_signal_order_delivered(),
            OrderStatus.CANCELED.value: lambda: self.order.send_signal_canceled(),
        }

        func = switcher.get(self.status, lambda: "Invalid status")
        func()
