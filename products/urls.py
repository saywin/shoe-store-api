from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CategoryView, ProductView, StockView

app_name = "products"

router = DefaultRouter()
router.register("category", CategoryView)
router.register("shoe", ProductView)
router.register("stock", StockView)

urlpatterns = [
    path("", include(router.urls))
]

