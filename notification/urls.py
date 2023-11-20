from django.urls import path
from rest_framework.routers import DefaultRouter

from notification.views import SendNotificationTestView, SendTestPushNotificationView

router = DefaultRouter()

urlpatterns = [
    path(
        "send-sms",
        SendNotificationTestView.as_view(),
        name="send-notification",
    ),
    path(
        "send-push-notification",
        SendTestPushNotificationView.as_view(),
        name="send-test-push-notification",
    ),
]

urlpatterns += router.urls
