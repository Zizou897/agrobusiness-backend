from authentication.exceptions import (
    OldPasswordNotCorrectError,
    OldPaswwordAndNewPasswordAreSameError,
)
from authentication.models import User


class ChangePasswordUsecase:
    @staticmethod
    def execute(user: User, old_password: str, new_password: str):
        if user.check_password(old_password) is False:
            raise OldPasswordNotCorrectError()

        if user.check_password(new_password) is True:
            raise OldPaswwordAndNewPasswordAreSameError()

        user.set_password(new_password)
        user.save()
