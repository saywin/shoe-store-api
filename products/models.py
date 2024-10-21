from django.db import models
from rest_framework.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категорія")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="subcategories",
        verbose_name="Підкатегорія",
    )
    slug = models.SlugField(
        max_length=255, blank=True, unique=True, verbose_name="Url"
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="shop/category",
        verbose_name="Зображення",
    )

    class Meta:
        db_table = "category"
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Name: {self.name}, slug: {self.slug}, parent: {self.parent}"


class Size(models.Model):
    size = models.CharField(max_length=5, verbose_name="Розмір")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення"
    )
    update_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата оновлення"
    )

    class Meta:
        db_table = "size"
        verbose_name = "Розмір"
        verbose_name_plural = "Розміри"

    def __str__(self):
        return self.size


class Product(models.Model):
    SEASON_CHOICES = {
        "AUTUMN": "Осінь",
        "SUMMER": "Літо",
        "WINTER": "Зима",
        "SPRING": "Весна",
    }

    name = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Ціна"
    )
    slug = models.SlugField(
        max_length=150, blank=True, unique=True, verbose_name="Url"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія",
    )
    color = models.CharField(max_length=50, verbose_name="Колір")
    article = models.CharField(max_length=30, verbose_name="Артикул")
    material = models.CharField(max_length=100, verbose_name="Матеріал")
    season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        default="WINTER",
        verbose_name="Сезон",
    )
    brand = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Бренд"
    )
    count = models.PositiveIntegerField(default=0, verbose_name="Кількість")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата оновлення"
    )

    class Meta:
        db_table = "product"
        verbose_name = "Взуття"
        verbose_name_plural = "Взуття"
        ordering = ["-created_at", "updated_at"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Name: {self.name}, price: {self.price}, color: {self.color}"


class Stock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="stocks"
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name="stocks",
        verbose_name="Розмір"
    )
    quantity = models.IntegerField(verbose_name="Кількість")

    def clean(self):
        total_quantity_in_stock = sum(stock.quantity for stock in self.product.stocks.exclude(pk=self.pk))

        if total_quantity_in_stock + self.quantity > self.product.count:
            raise ValidationError(
                "Сумарна кількість товарів у складі не може перевищувати загальну кількість продукту.")

    class Meta:
        db_table = "stock"
        constraints = [models.UniqueConstraint(
            fields=["product", "size"], name="unique_product_size"
        )]

    def __str__(self):
        return f"{self.product.name} - {self.size.size}, quantity: {self.quantity}"


class Gallery(models.Model):
    image = models.ImageField(upload_to="products/", verbose_name="Зображення")
    products = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Продукт"
    )

    class Meta:
        db_table = "gallery"
        verbose_name = "Зображення"
        verbose_name_plural = "Галерея товарів"

    def __str__(self):
        return f"{self.products.name} - {self.image}"
