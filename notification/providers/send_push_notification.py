from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from notification.utils.send_notification import Notification


class SendPushNotification(Notification):
    def __init__(self, user_id: str, message: Message):
        self.user_id = user_id
        self.message = message

    def send(self) -> None:
        device_exist = FCMDevice.objects.filter(user_id=self.user_id).exists()
        if device_exist:
            device = FCMDevice.objects.get(user_id=self.user_id)
            device.send_message(message=self.message)

