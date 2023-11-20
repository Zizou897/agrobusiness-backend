from celery import shared_task

from notification.use_cases.send_notification_order_created_use_case import SendNotificationOrderCreatedUseCase
from notification.use_cases.send_reset_password_email_use_case import (
    SendResetPasswordEmailUseCase,
)
from notification.use_cases.send_verification_email_use_case import (
    SendVerificationEmailUseCase,
)


@shared_task
def send_mail_verification(user_id, otp_code):
    SendVerificationEmailUseCase.execute(user_id, otp_code)


@shared_task
def send_mail_reset_password(user_id, otp_code):
    SendResetPasswordEmailUseCase.execute(user_id, otp_code)


@shared_task
def send_sms_order_created(order_id: str):
    send_notification_order_created_use_case = SendNotificationOrderCreatedUseCase(order_id)
    send_notification_order_created_use_case.execute()
