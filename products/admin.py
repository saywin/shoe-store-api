from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Category, Product, Gallery, Stock, Size


class GalleryInline(admin.TabularInline):
    pk_name = "product"
    model = Gallery
    extra = 1


class StockInline(admin.TabularInline):
    pk_name = "product"
    model = Stock
    extra = 1
    fields = ["size", "quantity"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["get_picture", "name", "parent", "get_category_count"]
    readonly_fields = ["get_picture"]
    prepopulated_fields = {"slug": ("name", )}

    def get_picture(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50'>")
        else:
            return "---"

    def get_category_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))

    get_picture.short_description = "Мініатюра"
    get_category_count.short_description = "Кількість товарів"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["get_image", "pk", "name", "description", "price", "count", "color", "category", "created_at"]
    readonly_fields = ["get_image"]
    prepopulated_fields = {"slug": ("name", )}
    list_editable = ["price", "count", "color"]
    list_filter = ["price", "name"]
    list_display_links = ["pk", "name"]
    inlines = (GalleryInline, StockInline)

    def get_image(self, obj):
        if obj.images.all():
            return mark_safe(f"<img src='{obj.images.all()[0].image.url}', width='70'>")
        else:
            return "---"

    get_image.short_description = "Фото"


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["size"]


@admin.register(Stock)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["quantity"]
