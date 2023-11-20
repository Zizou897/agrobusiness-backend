from django.dispatch import receiver
from notification.tasks import (
    send_mail_reset_password,
    send_notification_order_canceled,
    send_notification_order_confirmed,
    send_notification_order_created,
    send_notification_order_delivered,
    send_notification_order_ready_to_deliver,
)
from notification.use_cases.generate_otp_code_use_case import GenererCodeOTPUsecase
from notification.signals import (
    user_registered,
    reset_password_request,
    order_created,
    order_confirmed,
    order_delivered,
    order_canceled,
    order_ready_to_deliver,
)


@receiver(reset_password_request)
def handle_reset_password_request(sender, **kwargs):
    user_id = kwargs["user_id"]
    otp_code = GenererCodeOTPUsecase.execute(user_id)
    send_mail_reset_password.delay(user_id, otp_code)


@receiver(user_registered)
def handle_user_registered(sender, **kwargs):
    user_id = kwargs["user_id"]
    otp_code = GenererCodeOTPUsecase.execute(user_id)
    send_mail_reset_password.delay(user_id, otp_code)


@receiver(order_created)
def handle_order_created(sender, **kwargs):
    order_id = kwargs["order_id"]
    send_notification_order_created.delay(order_id)


@receiver(order_confirmed)
def handle_order_confirmed(sender, **kwargs):
    order_id = kwargs["order_id"]
    send_notification_order_confirmed.delay(order_id)


@receiver(order_delivered)
def handle_order_delivered(sender, **kwargs):
    order_id = kwargs["order_id"]
    send_notification_order_delivered.delay(order_id)


@receiver(order_canceled)
def handle_order_canceled(sender, **kwargs):
    order_id = kwargs["order_id"]
    send_notification_order_canceled.delay(order_id)


@receiver(order_ready_to_deliver)
def handle_order_ready_to_deliver(sender, **kwargs):
    order_id = kwargs["order_id"]
    send_notification_order_ready_to_deliver.delay(order_id)
