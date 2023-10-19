from django.db import transaction
from django.db.models import Q
from authentication.exceptions import (
    UsernameOrEmailAlreadyExistsError,
)
from authentication.models import User
from notification.use_cases.generate_otp_code_use_case import GenererCodeOTPUsecase
from notification.tasks import send_mail_verification


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

        otp_code = GenererCodeOTPUsecase().execute(user.id)
        transaction.on_commit(lambda: send_mail_verification.delay(user.id, otp_code))
        return user
