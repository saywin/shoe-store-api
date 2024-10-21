from rest_framework import viewsets

from products.models import Category, Product, Stock
from products.serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    StockListSerializer,
    StockDetailSerializer
)


class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer


class StockView(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return StockListSerializer
        if self.action == "retrieve":
            return StockDetailSerializer
