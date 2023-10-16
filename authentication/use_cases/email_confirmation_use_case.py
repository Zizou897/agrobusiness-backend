from authentication.exceptions import CodeNotCorrectError
from authentication.models import User
from authentication.use_cases.verify_otp_code_use_case import VerifyCodeOTPUsecase


class EmailConfirmationUseCase:
    @staticmethod
    def execute(**kwargs):
        code = kwargs.get('code')
        email = kwargs.get('email')

        # Vérifier si l'e-mail existe dans la base de données et est non vérifié
        user = User.objects.filter(email=email, is_verified=False).first()

        if user:
            use_case = VerifyCodeOTPUsecase()
            is_valid = use_case.execute(code=code, user_id=user.id)
            if is_valid:
                # Marquer l'utilisateur comme vérifié sans appeler save explicitement
                User.objects.filter(pk=user.id).update(is_verified=True)
                return user.id
            else:
                raise CodeNotCorrectError
        else:
            raise CodeNotCorrectError


