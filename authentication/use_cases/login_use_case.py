from django.contrib.auth import authenticate
from authentication.exceptions import (
    LoginFailedError,
    UserRegistrationNotCompleteError,
)
from authentication.models import User


class LoginUseCase:
    @staticmethod
    def execute(username: str, password: str) -> User:
        user = authenticate(username=username, password=password)
        if not user:
            raise LoginFailedError

        if not user.is_active:
            raise LoginFailedError

        if not user.is_verified:
            raise UserRegistrationNotCompleteError

        return user
