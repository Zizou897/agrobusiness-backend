from celery import shared_task
from notification.use_cases.send_notification_order_canceled_use_case import SendNotificationOrderCanceledUseCase
from notification.use_cases.send_notification_order_confirmed_use_case import SendNotificationOrderConfirmedUseCase

from notification.use_cases.send_notification_order_created_use_case import SendNotificationOrderCreatedUseCase
from notification.use_cases.send_notification_order_delivered_use_case import SendNotificationOrderDeliveredUseCase
from notification.use_cases.send_notification_order_ready_to_deliver_use_case import \
    SendNotificationOrderReadyToDeliverUseCase
from notification.use_cases.send_reset_password_email_use_case import (
    SendResetPasswordEmailUseCase,
)
from notification.use_cases.send_verification_email_use_case import (
    SendVerificationEmailUseCase,
)
from notification.utils.notification_channel_enums import NotificationChannelEnum


@shared_task
def send_mail_verification(user_id, otp_code):
    SendVerificationEmailUseCase.execute(user_id, otp_code)


@shared_task
def send_mail_reset_password(user_id, otp_code):
    SendResetPasswordEmailUseCase.execute(user_id, otp_code)


@shared_task
def send_notification_order_created(order_id: str):
    channels = [NotificationChannelEnum.PUSH.value]
    send_notification_order_created_use_case = SendNotificationOrderCreatedUseCase(order_id, channels)
    send_notification_order_created_use_case.execute()


@shared_task
def send_notification_order_confirmed(order_id: str):
    channels = [NotificationChannelEnum.PUSH.value]
    send_notification_order_confirmed_use_case = SendNotificationOrderConfirmedUseCase(order_id, channels)
    send_notification_order_confirmed_use_case.execute()


@shared_task
def send_notification_order_delivered(order_id: str):
    channels = [NotificationChannelEnum.PUSH.value]
    send_notification_order_delivered_use_case = SendNotificationOrderDeliveredUseCase(order_id, channels)
    send_notification_order_delivered_use_case.execute()


@shared_task
def send_notification_order_canceled(order_id: str):
    channels = [NotificationChannelEnum.PUSH.value]
    send_notification_order_canceled_use_case = SendNotificationOrderCanceledUseCase(order_id, channels)
    send_notification_order_canceled_use_case.execute()


@shared_task
def send_notification_order_ready_to_deliver(order_id: str):
    channels = [NotificationChannelEnum.PUSH.value]
    send_notification_order_ready_to_deliver_use_case = SendNotificationOrderReadyToDeliverUseCase(order_id, channels)
    send_notification_order_ready_to_deliver_use_case.execute()
