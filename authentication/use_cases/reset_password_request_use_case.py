from authentication.models import User
from notification.signals import reset_password_request
from notification.tasks import send_mail_reset_password
from notification.use_cases.generate_otp_code_use_case import GenererCodeOTPUsecase


class ResetPasswordRequestUseCase:
    def execute(self, email: str):
        user = User.objects.filter(email=email).first()

        if user:
            otp_code = GenererCodeOTPUsecase().execute(user.id)
            send_mail_reset_password.delay(user.id, otp_code)
