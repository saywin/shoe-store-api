from rest_framework import serializers

from products.models import Category, Product, Stock, Gallery, Size


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "slug", "image"]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size']


class StockSerializer(serializers.ModelSerializer):
    size = serializers.SlugRelatedField(read_only=True, slug_field="size")

    class Meta:
        model = Stock
        fields = ["id", 'size', 'quantity']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", 'image']


class ProductListSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True)
    first_image = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "category",
            "color",
            "article",
            "season",
            "stocks",
            "first_image",
        ]

    def get_first_image(self, obj):
        request = self.context.get("request")
        if obj.images.exists():
            first_image = obj.images.first()
            image_url = first_image.image.url
            return request.build_absolute_uri(image_url)
        return "https://img.freepik.com/premium-vector/photo-coming-soon-picture-frame-neon-sign_100456-4588.jpg"


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    stocks = StockSerializer(many=True, read_only=False)
    images = GallerySerializer(many=True, read_only=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "slug",
            "color",
            "article",
            "material",
            "season",
            "brand",
            "count",
            "created_at",
            "updated_at",
            "category",
            "stocks",
            "images",
        ]


class StockListSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(read_only=True, slug_field="name")
    article = serializers.SerializerMethodField()
    size = serializers.SlugRelatedField(read_only=True, slug_field="size")

    class Meta:
        model = Stock
        fields = "__all__"

    def get_article(self, obj):
        return obj.product.article


class StockDetailSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    size = SizeSerializer()

    class Meta:
        model = Stock
        fields = ["id", "product", "size", "quantity"]
