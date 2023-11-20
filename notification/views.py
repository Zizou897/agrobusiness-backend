from rest_framework.response import Response
from rest_framework.views import APIView
from notification.providers.send_push_notification import SendPushNotification
from notification.providers.send_sms_notificaton import SendSMSNotification
from notification.utils.push_notification_builder import PushNotificationDataBuilder
from notification.utils.send_notification import SendNotification


# Create your views here.
class SendNotificationTestView(APIView):
    def post(self, request):
        send_sms_notification = SendSMSNotification(sender="Agrijeune")
        send_notification = SendNotification(send_sms_notification)
        send_notification.sms("+2250779985122", "Hello world")
        return Response({"message": "Notification sent"})


class SendTestPushNotificationView(APIView):
    def post(self, request):
        builder = PushNotificationDataBuilder()
        message = builder.set_title("Nouvelle commande") \
            .set_body("Une nouvelle commande a été passée.") \
            .set_data({"type": "order"}) \
            .build()
        user_id = 'aa1497a2-ba7c-45bf-a229-6370c8c2557c'
        push_notification = SendPushNotification(user_id, message)
        send_notification = SendNotification(push_notification)
        send_notification.push_notification()
        return Response({"message": "Notification sent"})


class SendTestWhatsappNotificationView(APIView):
    def post(self, request):
        pass
