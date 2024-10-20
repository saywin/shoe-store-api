from rest_framework import serializers

from products.models import Category, Product, Stock, Gallery, Size
import logging

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "slug", "image"]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id"]


class StockSerializer(serializers.ModelSerializer):
    size = SizeSerializer(many=True)

    class Meta:
        model = Stock
        fields = ["size", "quantity"]

    def create(self, validated_data):
        size_data = validated_data.pop('size')
        size_instance = Size.objects.get(size=size_data)
        stock = Stock.objects.create(size=size_instance, **validated_data)
        return stock


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["image"]


class ProductSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, write_only=True)
    images = GallerySerializer(many=True, write_only=True)
    print(stocks)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "slug",
            "color",
            "article",
            "material",
            "season",
            "brand",
            "count",
            "created_at",
            "updated_at",
            "stocks",
            "images",
        ]

    def create(self, validated_data):
        sizes_data = validated_data.pop('stocks')
        images_data = validated_data.pop('images')

        logger.info("Validated Data: %s", validated_data)
        logger.info("Sizes data: %s", sizes_data)
        logger.info("Images data: %s", images_data)

        product = Product.objects.create(**validated_data)

        for size_data in sizes_data:
            Stock.objects.create(product=product, **size_data)

        for image_data in images_data:
            Gallery.objects.create(products=product, **image_data)

        return product
