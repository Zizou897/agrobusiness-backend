from rest_framework.generics import get_object_or_404
from authentication.models import User
from notification.send_notification import SendNotification


class SendVerificationEmailUseCase:
    @staticmethod
    def execute(user_id: str, code: int):
        user = get_object_or_404(User, id=user_id)
        recepient_full_name = user.get_full_name()
        recepient_email = user.email
        username = user.username

        context = {
            "NOM_CLIENT": recepient_full_name,
            "OTP_CODE": code,
            "USERNAME": username,
        }

        SendNotification.mail(context, "email_verification", [recepient_email])
