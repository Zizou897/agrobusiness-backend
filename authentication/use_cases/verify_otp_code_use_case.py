from rest_framework.generics import get_object_or_404
from authentication.exceptions import CodeNotCorrectError
from authentication.hotp_verification import HotpVerification
from authentication.models import HOTPDevice


class VerifyCodeOTPUsecase:
    def __init__(self) -> None:
        self.hotp_verification = HotpVerification()

    def execute(self, code: str, user_id):
        hotp_device = get_object_or_404(HOTPDevice, user_id=user_id)
        is_verified = self.hotp_verification.verify_token(
            hotp_device.counter, code, hotp_device.key
        )
        if is_verified is False:
            raise CodeNotCorrectError
        else:
            hotp_device.counter += 1
            hotp_device.save()
            return True
