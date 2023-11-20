from advert.models import ProductOrder
from notification.providers.send_push_notification import SendPushNotification
from notification.providers.send_sms_notificaton import SendSMSNotification
from notification.utils.notification_channel_enums import NotificationChannelEnum
from notification.utils.notification_type_enums import NotificationTypeEnum
from notification.utils.push_notification_builder import PushNotificationDataBuilder
from notification.utils.send_notification import SendNotification


class SendNotificationOrderCanceledUseCase:
    def __init__(self, order_id, channels: list[NotificationChannelEnum]):
        self.order_id = order_id
        self.channels = channels

    def execute(self):
        order = ProductOrder.objects.get(id=self.order_id)
        order_reference = order.reference
        store_name = order.product.store.name
        data_builder = (
            PushNotificationDataBuilder()
            .set_title("Commande annulée")
            .set_data({"type": NotificationTypeEnum.order_canceled.value})
            .set_body(
                f"Bonjour {store_name}, "
                f"la commande"
                f" avec la référence "
                f"{order_reference} a été annulée par l'acheteur"
            )
            .set_data({"type": NotificationTypeEnum.order_canceled.value})
            .build()
        )

        for channel in self.channels:
            if channel == NotificationChannelEnum.PUSH.value:
                notification_push = SendPushNotification(order.user_id, data_builder)
                send_notification = SendNotification(notification_push)
                send_notification.push_notification()
            elif channel == NotificationChannelEnum.SMS.value:
                sms_notification = SendSMSNotification(sender="Agrijeune")
                seller = order.store.phone_number
                sms_notification.send(
                    to=seller,
                    text=f"Bonjour {store_name}, "
                         f"la commande"
                         f" avec la référence "
                         f"{order_reference} a été annulée par l'acheteur",
                )
            elif channel == NotificationChannelEnum.WHATSAPP.value:
                pass
            elif channel == NotificationChannelEnum.EMAIL.value:
                pass
            else:
                raise Exception("Channel not supported")
