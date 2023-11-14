from rest_framework.response import Response
from rest_framework.views import APIView

from notification.providers.send_sms_notificaton import SendSMSNotification
from notification.send_notification import SendNotification


# Create your views here.
class SendNotificationTestView(APIView):
    def post(self, request):
        send_sms_notification = SendSMSNotification(sender='Agrijeune')
        send_notification = SendNotification(send_sms_notification)
        send_notification.send_sms('+2250779985122', 'Hello world')
        return Response({'message': 'Notification sent'})
