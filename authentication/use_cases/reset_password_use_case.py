from rest_framework.generics import get_object_or_404
from authentication.exceptions import CodeNotCorrectError
from authentication.models import User
from authentication.use_cases.verify_otp_code_use_case import VerifyCodeOTPUsecase


class ResetPasswordUsecase:
    @staticmethod
    def execute(**kwargs):
        user_email = kwargs.get('email')
        password = kwargs.get('password')
        otp_code = kwargs.get('code')

        user = get_object_or_404(User, email=user_email)
        use_case = VerifyCodeOTPUsecase()

        is_correct = use_case.execute(otp_code, user.id)

        if is_correct is False:
            raise CodeNotCorrectError

        user.set_password(password)
        user.save()
        return user
