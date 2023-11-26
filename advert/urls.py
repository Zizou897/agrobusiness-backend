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
router.register(r"seller-delivery", SellerDeliveryView, basename="delivery")

urlpatterns = [
    path("seller/products/", VendorProductListView.as_view(), name="seller-products"),
    path("favorites/", ProductFavoritesListView.as_view(), name="favorites"),
    path("orders/<uuid:pk>/", ProductOrderUpdateStatusView.as_view(), name="update-order-status"),
    path("orders/", ProductOrderListView.as_view(), name="orders"),
    path("seller/statistics/", SellerStatisticsAPIView.as_view(), name="seller-statistics"),
    path("seller/weekly-sales/", WeeklySalesAPIView.as_view(), name="seller-weekly-sales"),
]

urlpatterns += router.urls
