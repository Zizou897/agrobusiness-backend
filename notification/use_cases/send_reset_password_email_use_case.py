from rest_framework.generics import get_object_or_404
from templated_mail.mail import BaseEmailMessage
from authentication.models import User


class SendResetPasswordEmailUseCase:
    @staticmethod
    def execute(user_id, code: int):
        user = get_object_or_404(User, id=user_id)

        recepient_full_name = user.get_full_name()
        recepient_email = user.email
        recepient_username = user.username

        context = {
            'RECIPIENT_NAME': recepient_full_name,
            'OTP_CODE': code,
            'USERNAME': recepient_username,
        }
        html_message = BaseEmailMessage(
            template_name='reset_password.html',
            context=context
        )
        return html_message.send(to=[recepient_email])
