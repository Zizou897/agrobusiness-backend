import pyotp as pyotp


class HotpVerification:
    @staticmethod
    def generate_key():
        return pyotp.random_base32(length=64)

    @staticmethod
    def generate_token(counter: int, keygen: str):
        totp = pyotp.HOTP(keygen)
        otp = totp.at(counter)
        return otp

    @staticmethod
    def verify_token(counter: int, otp: str, key: str):
        totp = pyotp.HOTP(key)
        return totp.verify(str(otp), counter)
