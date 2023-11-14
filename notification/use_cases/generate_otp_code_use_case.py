from authentication.hotp_verification import HotpVerification
from authentication.models import HOTPDevice


class GenererCodeOTPUsecase:
    @staticmethod
    def execute(user_id: str):
        # Vérifier si l'utilisateur a déjà un device HOTP
        hotp_device, created = HOTPDevice.objects.get_or_create(user_id=user_id)

        # Génerer une clé HOTP
        key = HotpVerification.generate_key()

        # Sauvegarder la clé HOTP
        hotp_device.key = key
        hotp_device.counter += 1

        hotp_device.save(update_fields=["key", "counter"])

        updated_hotp_device = HOTPDevice.objects.get(user_id=user_id)

        # Générer le code OTP
        otp_token = HotpVerification.generate_token(
            updated_hotp_device.counter, updated_hotp_device.key
        )

        return otp_token
