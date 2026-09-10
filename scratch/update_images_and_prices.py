import os
import sys
import shutil
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weddingcards.settings")
django.setup()

from catalog.models import Category, Design

images1_dir = os.path.join(base_dir, "images1")
media_dir = os.path.join(base_dir, "media", "designs")

os.makedirs(media_dir, exist_ok=True)

# List all files in images1
image_files = sorted([f for f in os.listdir(images1_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))])

print(f"Found {len(image_files)} images in images1.")

# Clean copy to media/designs/
copied_files = []
for idx, fname in enumerate(image_files, 1):
    ext = os.path.splitext(fname)[1]
    new_name = f"invitation_{idx:02d}{ext}"
    src_path = os.path.join(images1_dir, fname)
    dst_path = os.path.join(media_dir, new_name)
    shutil.copy2(src_path, dst_path)
    copied_files.append(f"designs/{new_name}")

print(f"Copied {len(copied_files)} images to media/designs/")

# Curated design details related to real invitation styles
design_catalog_data = [
    {
        "name": "Siddhi Ganesha Gold Hot-Foil Suite",
        "subtitle": "Includes 3 Gold Leaf Inserts, Embossed Outer Envelope & Wax Seal",
        "description": "Handcrafted ceremonial wedding card featuring rich gold hot-foil Ganesha emblem on heavy 600 GSM Italian cardstock. Complete with silk drawstring pouch.",
        "price": 145.00,
        "sku": "SV-101",
        "badge": "Bestseller",
        "tradition": "hindu",
        "craft_style": "gold_foil",
        "color": "gold"
    },
    {
        "name": "Crimson & Gold Royal Gatefold Suite",
        "subtitle": "Laser Cut Door Opening with Velvet Finish Inserts",
        "description": "Exquisite door-opening gatefold invitation crafted in royal crimson maroon with metallic gold foil accents and intricate Balaji motif.",
        "price": 185.00,
        "sku": "SV-102",
        "badge": "Trending",
        "tradition": "hindu",
        "craft_style": "gatefold",
        "color": "maroon"
    },
    {
        "name": "Royal Peacock Sacred Floral Card",
        "subtitle": "Multicolor Offset Printing with Embossed Peacock Motif",
        "description": "Elegant traditional invitation adorned with vibrant peacock feathers, gold foil leafing, and botanical floral borders.",
        "price": 95.00,
        "sku": "SV-103",
        "badge": "New",
        "tradition": "hindu",
        "craft_style": "gold_foil",
        "color": "green"
    },
    {
        "name": "Raw Silk Padded Hardcover Box Suite",
        "subtitle": "Padded Box with 4 Acrylic Inserts & Sweet Box Pouch",
        "description": "Luxurious raw silk padded hardcover invitation box with gold die-cut monogram frame, matching sweet jar pouches, and golden tassel ties.",
        "price": 320.00,
        "sku": "SV-104",
        "badge": "Luxe Collection",
        "tradition": "hindu",
        "craft_style": "padded_velvet",
        "color": "gold"
    },
    {
        "name": "Imperial Scroll Farman Royal Suite",
        "subtitle": "Hand-Rolled Silk Scroll in Brass-Finished Velvet Box",
        "description": "Royal Farman scroll invitation printed on heavy textured silk fabric with brass end knobs, housed in an embroidered velvet box.",
        "price": 450.00,
        "sku": "SV-105",
        "badge": "Heritage Classic",
        "tradition": "interfaith",
        "craft_style": "padded_velvet",
        "color": "maroon"
    },
    {
        "name": "Pista Green Botanical Mandala Card",
        "subtitle": "2 Floral Printed Inserts & Gold Foil Border Envelope",
        "description": "Modern serene pista green wedding invitation with delicate botanical mandala foiling and golden metallic typography.",
        "price": 110.00,
        "sku": "SV-106",
        "badge": "Popular",
        "tradition": "hindu",
        "craft_style": "gold_foil",
        "color": "green"
    },
    {
        "name": "Ivory Pearl Laser-Cut Door Invitation",
        "subtitle": "3 Layered Textured Inserts with Satin Ribbon Lacing",
        "description": "Ultra-fine laser-cut filigree door invitation on ivory pearl cardstock with champagne gold foil stamping and silk ribbon closure.",
        "price": 165.00,
        "sku": "SV-107",
        "badge": "Elegant Pick",
        "tradition": "christian",
        "craft_style": "laser_cut",
        "color": "cream"
    },
    {
        "name": "Deep Ruby Velvet Padded Folio Card",
        "subtitle": "Gold Die-Cut Emblem Frame & 3 Gilded Edge Inserts",
        "description": "Premium velvet padded folio card in deep ruby red featuring customized die-cut initial emblem and gold gilded insert edges.",
        "price": 240.00,
        "sku": "SV-108",
        "badge": "Royal Special",
        "tradition": "hindu",
        "craft_style": "padded_velvet",
        "color": "maroon"
    },
    {
        "name": "Auspicious Radha Krishna Serenade Card",
        "subtitle": "UV Embossed Art Print with Gold Hot-Stamping",
        "description": "Sacred wedding invitation featuring divine Radha Krishna UV embossed artwork surrounded by intricate temple pillar motifs.",
        "price": 135.00,
        "sku": "SV-109",
        "badge": "Auspicious",
        "tradition": "hindu",
        "craft_style": "gold_foil",
        "color": "gold"
    },
    {
        "name": "Powder Blue Royal Brocade Invitation",
        "subtitle": "Brocade Fabric Pocket Cover & 2 Silver Foil Inserts",
        "description": "Chic powder blue brocade texture invitation with silver hot-foil accents and personalized couple crest seal.",
        "price": 175.00,
        "sku": "SV-110",
        "badge": "Modern Royal",
        "tradition": "interfaith",
        "craft_style": "gatefold",
        "color": "blue"
    },
    {
        "name": "Rose Pink Botanical Chanderi Suite",
        "subtitle": "Chanderi Patterned Cover & 3 Pastel Foil Inserts",
        "description": "Soft rose pink wedding card styled with traditional Chanderi weave patterns, gold leaf motifs, and matching sweet boxes.",
        "price": 155.00,
        "sku": "SV-111",
        "badge": "Designer Choice",
        "tradition": "hindu",
        "craft_style": "gold_foil",
        "color": "pink"
    },
    {
        "name": "Rotating Wheel Shubh Muhurat Card",
        "subtitle": "Interactive Rotating Wheel Mechanism & 3 Inner Leaflets",
        "description": "Unique interactive rotating wheel wedding card revealing auspicious ceremony dates and times with golden foil details.",
        "price": 195.00,
        "sku": "SV-112",
        "badge": "Innovative",
        "tradition": "hindu",
        "craft_style": "rotating",
        "color": "gold"
    },
]

# Update database
cat_main, _ = Category.objects.get_or_create(name="All Invitations")

# Clear old designs or update them
Design.objects.all().delete()

for i, rel_path in enumerate(copied_files):
    # Select metadata from design_catalog_data cyclically or construct dynamically
    meta = design_catalog_data[i % len(design_catalog_data)]
    
    name = f"{meta['name']} #{i+1:02d}"
    
    design = Design.objects.create(
        name=name,
        subtitle=meta["subtitle"],
        description=meta["description"],
        image=rel_path,
        price=meta["price"] + (i * 5),
        original_price=None,  # KEEP ONLY PRICE (no original_price)
        sku=f"SV-{100+i+1}",
        badge=meta["badge"],
        rating=4.9,
        reviews_count=120 + i * 5,
        is_sale=False,
        is_new=(i < 6),
        is_luxe=(meta["price"] > 200),
        tradition=meta["tradition"],
        craft_style=meta["craft_style"],
        color=meta["color"],
        category=cat_main
    )
    print(f"Created design: {design.name} with image {rel_path} and price RS {design.price}")

print("Successfully updated all designs with images from images1 and set original_price to None!")
