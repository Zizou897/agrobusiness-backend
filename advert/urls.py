from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductOrderListView,
    ProductOrderUpdateStatusView,
    ProductFavoritesListView,
    ProductsSectionView,
    VendorProductListView,
    SellerStatisticsAPIView,
    WeeklySalesAPIView,
    SellerDeliveryView
)
from django.urls import path

router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="products")
router.register(r"sections", ProductsSectionView, basename="sections")
router.register(r"vendor-delivery", SellerDeliveryView, basename="delivery")

urlpatterns = [
    path("vendor/products/", VendorProductListView.as_view()),
    path("favorites/", ProductFavoritesListView.as_view()),
    path("orders/<uuid:pk>/", ProductOrderUpdateStatusView.as_view()),
    path("orders/", ProductOrderListView.as_view()),
    path("seller/statistics/", SellerStatisticsAPIView.as_view()),
    path("seller/weekly-sales/", WeeklySalesAPIView.as_view()),
]

urlpatterns += router.urls
