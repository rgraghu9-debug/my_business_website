"""
Management command to seed sample categories and designs for development.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from catalog.models import Category, Design
from decimal import Decimal


CATEGORIES = [
    "Royal & Traditional",
    "Floral & Botanical",
    "Minimalist & Modern",
    "Destination Wedding",
]

DESIGNS = [
    {
        "name": "Golden Paisley Elegance",
        "description": (
            "A regal design featuring intricate golden paisley patterns against a deep "
            "crimson background. Perfect for traditional Hindu weddings seeking a luxurious feel."
        ),
        "price": Decimal("1500.00"),
        "category": "Royal & Traditional",
    },
    {
        "name": "Rose Blossom Romance",
        "description": (
            "Delicate watercolour roses cascade across ivory card stock, creating a soft "
            "and romantic aesthetic ideal for garden and outdoor weddings."
        ),
        "price": Decimal("1200.00"),
        "category": "Floral & Botanical",
    },
    {
        "name": "Ivory Minimal Chic",
        "description": (
            "Clean lines, generous white space, and tasteful gold foil typography — "
            "this understated design lets the details speak for themselves."
        ),
        "price": Decimal("900.00"),
        "category": "Minimalist & Modern",
    },
    {
        "name": "Tropical Breeze",
        "description": (
            "Sun, sand, and palm fronds set the tone for a destination beach wedding. "
            "Vibrant tropical illustrations on a cream linen-texture card."
        ),
        "price": Decimal("1100.00"),
        "category": "Destination Wedding",
    },
    {
        "name": "Marigold Mandap",
        "description": (
            "Inspired by the vibrant marigold flower arrangements of South Asian weddings, "
            "this bold and joyful design radiates celebration."
        ),
        "price": Decimal("1350.00"),
        "category": "Royal & Traditional",
    },
    {
        "name": "Verdant Garden",
        "description": (
            "Lush botanical greens with hand-drawn eucalyptus and fern illustrations "
            "frame your wedding details in natural, earthy sophistication."
        ),
        "price": Decimal("1050.00"),
        "category": "Floral & Botanical",
    },
]


class Command(BaseCommand):
    help = "Seed sample categories and designs (no images) for development"

    def handle(self, *args, **options):
        # Create categories
        cat_objects = {}
        for cat_name in CATEGORIES:
            cat, created = Category.objects.get_or_create(name=cat_name)
            cat_objects[cat_name] = cat
            verb = "Created" if created else "Already exists"
            self.stdout.write(f"  Category — {verb}: {cat_name}")

        # Create designs (no image — placeholder)
        count = 0
        for d in DESIGNS:
            if not Design.objects.filter(name=d["name"]).exists():
                Design.objects.create(
                    name=d["name"],
                    description=d["description"],
                    price=d["price"],
                    category=cat_objects[d["category"]],
                    # image is left blank — admin must upload
                )
                self.stdout.write(f"  Design  — Created: {d['name']}")
                count += 1
            else:
                self.stdout.write(f"  Design  — Already exists: {d['name']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeed complete. {count} new designs created."
            )
        )
