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
        fields = ['id', 'size']


class StockSerializer(serializers.ModelSerializer):
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all())

    class Meta:
        model = Stock
        fields = ['size', 'quantity']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, write_only=True)
    images = GallerySerializer(many=True, write_only=True)

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
        stocks_data = validated_data.pop('stocks')
        images_data = validated_data.pop('images')

        logger.info("Validated Data: %s", validated_data)
        logger.info("Sizes data: %s", stocks_data)
        logger.info("Images data: %s", images_data)

        product = Product.objects.create(**validated_data)

        for stock_data in stocks_data:
            Stock.objects.create(product=product, **stock_data)

        for image_data in images_data:
            Gallery.objects.create(product=product, **image_data)

        return product
