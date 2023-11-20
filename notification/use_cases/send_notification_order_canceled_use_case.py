from advert.models import ProductOrder
from notification.utils.notification_channel_enums import NotificationChannelEnum


class SendNotificationOrderCanceledUseCase:
    def __init__(self, order_id, channels: list[NotificationChannelEnum]):
        self.order_id = order_id
        self.channels = channels

    def execute(self):
        order = ProductOrder.objects.get(id=self.order_id)


