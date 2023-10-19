from django.dispatch import receiver
from notification.tasks import send_mail_reset_password
from notification.use_cases.generate_otp_code_use_case import GenererCodeOTPUsecase
from notification.signals import user_registered, reset_password_request, order_created, order_status_changed


@receiver(reset_password_request)
def handle_reset_password_request(sender, **kwargs):
    user_id = kwargs['user_id']
    otp_code = GenererCodeOTPUsecase.execute(user_id)
    send_mail_reset_password.delay(user_id, otp_code)


@receiver(user_registered)
def handle_user_registered(sender, **kwargs):
    user_id = kwargs['user_id']
    otp_code = GenererCodeOTPUsecase.execute(user_id)
    send_mail_reset_password.delay(user_id, otp_code)


@receiver(order_created)
def handle_order_created(sender, **kwargs):
    order_id = kwargs['order_id']
    # Send notification to seller
    # Send notification to buyer


@receiver(order_status_changed)
def handle_order_status_changed(sender, **kwargs):
    order_id = kwargs['order_id']
    # Send notification to seller
    # Send notification to buyer
