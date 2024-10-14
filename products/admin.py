from django.contrib import admin

from products.models import Category, Product, Gallery, Stock


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
    list_display = ["name", "parent"]
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "description", "price", "count", "color", "category", "created_at"]
    prepopulated_fields = {"slug": ("name", )}
    list_editable = ["price", "count", "color"]
    list_filter = ["price", "name"]
    list_display_links = ["pk", "name"]
    inlines = (GalleryInline, StockInline)
