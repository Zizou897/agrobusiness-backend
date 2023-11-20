from django.db import transaction
from django.db.models import Q
from authentication.exceptions import (
    UsernameOrEmailAlreadyExistsError,
)
from authentication.models import User
from notification.signals import user_registered
from notification.use_cases.generate_otp_code_use_case import GenererCodeOTPUsecase
from notification.tasks import send_mail_verification
from notification.use_cases.send_verification_email_use_case import SendVerificationEmailUseCase


class RegisterUserUseCase:
    @transaction.atomic
    def execute(self, **kwargs):
        email = kwargs.get("email")
        username = kwargs.get("username")
        password = kwargs.get("password")
        profil_type = kwargs.get("profil_type")
        phone_number = kwargs.get("phone_number")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        country = kwargs.get("country")

        user = User.objects.filter(Q(email=email) | Q(username=username)).first()

        if user:
            raise UsernameOrEmailAlreadyExistsError()

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            profil_type=profil_type,
            country=country,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        transaction.on_commit(lambda: user_registered.send(sender=self.__class__, user_id=user.id))
        return user
