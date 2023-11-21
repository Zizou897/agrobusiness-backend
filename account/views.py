from rest_framework.viewsets import ModelViewSet
from account.models import Store
from account.use_cases.save_fcm_device_use_case import SaveFCMDeviceUseCase
from account.serializers import FCMDeviceSerializer
from .serializers import StoreSerializer, StoreCreateSerializer
from .filters import StoreFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from fcm_django.models import FCMDevice


class StoreView(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filterset_class = StoreFilter

    def get_serializer_class(self):
        if self.action in ["create", "put", "patch"]:
            return StoreCreateSerializer
        return StoreSerializer


class FCMDeviceView(CreateAPIView):
    serializer_class = FCMDeviceSerializer
    queryset = FCMDevice.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        type = serializer.validated_data["type"]
        user = serializer.validated_data["user"]
        name = serializer.validated_data["name"]
        registration_id = serializer.validated_data["registration_id"]
        device_id = serializer.validated_data["device_id"]

        SaveFCMDeviceUseCase.execute(
            user=user,
            type=type,
            name=name,
            registration_id=registration_id,
            device_id=device_id,
        )
        return Response(status=status.HTTP_200_OK)
