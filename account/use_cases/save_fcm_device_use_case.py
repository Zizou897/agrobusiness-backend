from fcm_django.models import FCMDevice

from authentication.models import User


class SaveFCMDeviceUseCase:
    @staticmethod
    def execute(**kwargs):
        registration_id = kwargs.get("registration_id")
        device_id = kwargs.get("device_id")
        type = kwargs.get("type")
        user: User = kwargs.get("user")
        name = kwargs.get("name")

        device_exist = FCMDevice.objects.filter(registration_id=registration_id, active=True).exists()
        if device_exist:
            return FCMDevice.objects.get(registration_id=registration_id)
        else:
            device_is_inactive = FCMDevice.objects.filter(registration_id=registration_id, active=False).exists()
            if device_is_inactive:
                # remove the inactive device
                FCMDevice.objects.filter(registration_id=registration_id, active=False).delete()
            device = FCMDevice.objects.create(
                registration_id=registration_id,
                user=user,
                name=name,
                device_id=device_id,
                type=type,
            )
            return device
