from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductOrderListView,
    ProductOrderUpdateStatusView,
    ProductFavoritesListView,
    ProductsSectionView,
    ProductCartDeleteView,
    ProductCartListView
)
from django.urls import path

router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="products")
router.register(r"sections", ProductsSectionView, basename="sections")

urlpatterns = [
    path("favorites/", ProductFavoritesListView.as_view()),
    path("orders/<uuid:pk>/status/", ProductOrderUpdateStatusView.as_view()),
    path("orders/", ProductOrderListView.as_view()),
    path("cart/", ProductCartListView.as_view()),
    path("cart/<uuid:pk>/delete", ProductCartDeleteView.as_view()),
]

urlpatterns += router.urls
