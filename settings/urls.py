from django.urls import path
from rest_framework.routers import DefaultRouter
from settings.views import (
    CategoryProductView,
    CountryView,
    MeasureView,
    PaymentMethodView,
    SectorView,
)


router = DefaultRouter()

router.register("category-product", CategoryProductView, basename="category-product")
router.register("sector", SectorView, basename="sector")
router.register("measure", MeasureView, basename="measure")
router.register("payment-method", PaymentMethodView, basename="payment-method")


urlpatterns = [
    path("countries/", CountryView.as_view(), name="countries"),
]

urlpatterns += router.urls
