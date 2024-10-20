from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CategoryView, ProductView

app_name = "products"

router = DefaultRouter()
router.register("category", CategoryView)
router.register("shoe", ProductView)

urlpatterns = [
    path("", include(router.urls))
]

