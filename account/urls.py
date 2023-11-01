from rest_framework.routers import DefaultRouter
from .views import StoreView


router = DefaultRouter()

router.register(r"store", StoreView, basename="store")

urlpatterns = []

urlpatterns += router.urls
