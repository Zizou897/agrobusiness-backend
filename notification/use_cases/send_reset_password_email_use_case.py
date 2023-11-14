from rest_framework.generics import get_object_or_404
from authentication.models import User
from notification.send_notification import SendNotification


class SendResetPasswordEmailUseCase:
    @staticmethod
    def execute(user_id, code: int):
        user = get_object_or_404(User, id=user_id)

        recepient_full_name = user.get_full_name()
        recepient_email = user.email
        recepient_username = user.username

        context = {
            "RECIPIENT_NAME": recepient_full_name,
            "OTP_CODE": code,
            "USERNAME": recepient_username,
        }
        SendNotification.mail(context, "reset_password", [recepient_email])
