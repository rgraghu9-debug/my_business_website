import json
import os
from pathlib import Path
from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Category, Design
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seeds all 31 real wedding invitation cards and categories for Siddhi Vinayak Cards"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting real catalog seeding..."))

        # 1. Clean up legacy mock/external googleusercontent designs
        deleted_count, _ = Design.objects.filter(image_url__icontains="googleusercontent").delete()
        if deleted_count:
            self.stdout.write(self.style.WARNING(f"Removed {deleted_count} legacy mock designs."))

        # Also remove old mock SKUs if present
        mock_skus = ["KAA06220", "RJT90441", "KRC31160", "KRC31070", "BLU88210", "GRY40120", 
                     "LAV55190", "OLV66240", "WHT11020", "GLD77310", "CRM22090", "BLU33410"]
        Design.objects.filter(sku__in=mock_skus).delete()

        # 2. Locate catalog_data.json
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        possible_paths = [
            Path(__file__).resolve().parent / "catalog_data.json",
            base_dir / "catalog_data.json",
        ]
        
        json_path = None
        for p in possible_paths:
            if p.exists():
                json_path = p
                break

        if not json_path:
            self.stdout.write(self.style.ERROR("catalog_data.json not found!"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 3. Create or update categories
        category_map = {}
        for item in data:
            if item.get("model") == "catalog.category":
                pk = item.get("pk")
                fields = item.get("fields", {})
                name = fields.get("name")
                slug = fields.get("slug") or slugify(name)
                cat, _ = Category.objects.update_or_create(
                    name=name,
                    defaults={"slug": slug}
                )
                category_map[pk] = cat
                category_map[name] = cat

        self.stdout.write(f"Processed {len(category_map)} categories.")

        # Ensure default "All Invitations" category exists
        default_cat, _ = Category.objects.get_or_create(
            name="All Invitations",
            defaults={"slug": "all-invitations"}
        )

        # 4. Create or update the 31 actual invitation designs
        design_count = 0
        for item in data:
            if item.get("model") == "catalog.design":
                fields = item.get("fields", {})
                sku = fields.get("sku")
                name = fields.get("name")
                cat_id = fields.get("category")
                category = category_map.get(cat_id) or default_cat

                # Ensure image path points to designs/invitation_XX.jpeg
                image_val = fields.get("image", "")

                design, created = Design.objects.update_or_create(
                    sku=sku,
                    defaults={
                        "name": name,
                        "subtitle": fields.get("subtitle", ""),
                        "description": fields.get("description", ""),
                        "image": image_val,
                        "image_url": "",  # Clear external image URLs to use local real photos
                        "price": Decimal(str(fields.get("price", "150.00"))),
                        "original_price": Decimal(str(fields["original_price"])) if fields.get("original_price") else None,
                        "badge": fields.get("badge", ""),
                        "rating": Decimal(str(fields.get("rating", "4.9"))),
                        "reviews_count": int(fields.get("reviews_count", 120)),
                        "is_sale": bool(fields.get("is_sale", False)),
                        "is_new": bool(fields.get("is_new", False)),
                        "is_luxe": bool(fields.get("is_luxe", False)),
                        "tradition": fields.get("tradition", "hindu"),
                        "craft_style": fields.get("craft_style", "gold_foil"),
                        "color": fields.get("color", "gold"),
                        "category": category,
                    }
                )
                design_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {design_count} real invitation designs!")
        )
