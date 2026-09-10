from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Design


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "design_count")
    search_fields = ("name",)

    def design_count(self, obj):
        return obj.designs.count()

    design_count.short_description = "Number of Designs"


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "badge", "image_preview", "created_at")
    list_filter = ("category", "is_new", "is_luxe", "created_at")
    search_fields = ("name", "sku", "description")
    list_editable = ("price", "badge")
    readonly_fields = ("image_preview", "created_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "sku",
                    "category",
                    "price",
                    "badge",
                    "subtitle",
                    "description",
                    "image",
                    "image_url",
                    "image_preview",
                )
            },
        ),
        (
            "Flags & Ratings",
            {
                "fields": ("is_sale", "is_new", "is_luxe", "rating", "reviews_count"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    def image_preview(self, obj):
        img_url = obj.get_image_url()
        if img_url:
            return format_html(
                '<img src="{}" style="max-height:120px; max-width:200px; '
                'border-radius:6px; object-fit:cover;" />',
                img_url,
            )
        return "No image"

    image_preview.short_description = "Preview"
