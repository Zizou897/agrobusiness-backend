from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductOrderListView,
    ProductOrderUpdateStatusView,
    ProductFavoritesListView,
)
from django.urls import path

router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("favorites/", ProductFavoritesListView.as_view()),
    path("orders/<uuid:pk>/status/", ProductOrderUpdateStatusView.as_view()),
    path("orders/", ProductOrderListView.as_view()),
]

urlpatterns += router.urls
