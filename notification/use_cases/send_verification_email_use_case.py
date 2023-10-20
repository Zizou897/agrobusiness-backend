from rest_framework.generics import get_object_or_404
from templated_mail.mail import BaseEmailMessage
from authentication.models import User


class SendVerificationEmailUseCase:
    @staticmethod
    def execute(user_id: str, code: int):
        user = get_object_or_404(User, id=user_id)
        recepient_full_name = user.get_full_name()
        recepient_email = user.email
        username = user.username

        context = {
            'NOM_CLIENT': recepient_full_name,
            'OTP_CODE': code,
            'USERNAME': username,
        }
        html_message = BaseEmailMessage(
            template_name='email_verification.html',
            context=context
        )
        return html_message.send(to=[recepient_email])
