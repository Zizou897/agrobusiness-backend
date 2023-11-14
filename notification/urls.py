from django.urls import path
from rest_framework.routers import DefaultRouter

from notification.views import SendNotificationTestView

router = DefaultRouter()

urlpatterns = [
    path(
        "send-notification",
        SendNotificationTestView.as_view(),
        name="send-notification",
    ),
]

urlpatterns += router.urls
