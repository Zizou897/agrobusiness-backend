from advert.models import ProductOrder
from notification.providers.send_push_notification import SendPushNotification
from notification.providers.send_sms_notificaton import SendSMSNotification
from notification.utils.notification_channel_enums import NotificationChannelEnum
from notification.utils.push_notification_builder import PushNotificationDataBuilder
from notification.utils.send_notification import SendNotification


class SendNotificationOrderCreatedUseCase:
    def __init__(self, order_id: str, channels: list[NotificationChannelEnum]):
        self.order_id = order_id
        self.channels = channels

    def execute(self):
        order = ProductOrder.objects.get(id=self.order_id)
        order_reference = order.reference
        store_name = order.product.store.name
        data_builder = (PushNotificationDataBuilder().set_title("Nouvelle commande")
                        .set_body(f"Bonjour {store_name}, "f"vous avez une commande"
                                  f" avec la référence "
                                  f"{order_reference}")
                        .set_topic("order_created")
                        .build())

        for channel in self.channels:
            if channel == NotificationChannelEnum.PUSH:
                notification_push = SendPushNotification(order.user_id, data_builder)
                send_notification = SendNotification(notification_push)
                send_notification.push_notification()
            elif channel == NotificationChannelEnum.SMS:
                sms_notification = SendSMSNotification(sender="Agrijeune")
                seller = order.store.phone_number
                sms_notification.send(to=seller, text=f"Bonjour {store_name}, "
                                                      f"vous avez reçu une nouvelle commande"
                                                      f" avec la référence {order_reference}, veuillez vous rendre "
                                                      f"sur l'application Agrijeune "
                                                      f"pour plus de détails, merci de votre confiance")
            elif channel == NotificationChannelEnum.WHATSAPP:
                pass
            elif channel == NotificationChannelEnum.EMAIL:
                pass
            else:
                raise Exception("Channel not supported")
