from rest_framework.viewsets import ModelViewSet
from account.models import Store
from .serializers import StoreSerializer, StoreCreateSerializer
from .filters import StoreFilter


class StoreView(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filterset_class = StoreFilter

    def get_serializer_class(self):
        if self.action in ["create", "put", "patch"]:
            return StoreCreateSerializer
        return StoreSerializer
