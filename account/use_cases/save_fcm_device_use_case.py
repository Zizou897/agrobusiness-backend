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

        try:
            device = FCMDevice.objects.get(registration_id=registration_id)

            # Verify if the device is already registered with the user
            if device.registration_id == registration_id and device.user == user:
                return device
            else:
                device.registration_id = registration_id
                device.user = user
                device.name = name
                device.device_id = device_id
                device.type = type
                device.save()
                return device
        except FCMDevice.DoesNotExist:
            device = FCMDevice.objects.create(
                registration_id=registration_id,
                user=user,
                name=name,
                device_id=device_id,
                type=type,
            )
        return device
