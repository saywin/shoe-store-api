from rest_framework import viewsets, mixins

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer


class CategoryView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
