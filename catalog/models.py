from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Design(models.Model):
    TRADITION_CHOICES = [
        ('hindu', 'Hindu Wedding'),
        ('muslim', 'Muslim Nikah'),
        ('christian', 'Christian Nuptials'),
        ('sikh', 'Sikh Anand Karaj'),
        ('interfaith', 'Interfaith / Fusion'),
    ]

    CRAFT_STYLE_CHOICES = [
        ('gold_foil', 'Gold Hot-Foil Stamping'),
        ('laser_cut', 'Laser Cut Filigree'),
        ('gatefold', 'Door & Gatefold Opening'),
        ('padded_velvet', 'Padded Velvet Hardcover'),
        ('rotating', 'Rotating Mechanism Card'),
    ]

    COLOR_CHOICES = [
        ('maroon', 'Crimson Maroon'),
        ('gold', 'Royal Gold'),
        ('cream', 'Ivory Cream'),
        ('green', 'Pista / Olive Green'),
        ('pink', 'Rose Pink'),
        ('blue', 'Powder Blue'),
    ]

    name = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True, help_text="e.g. Includes 3 Gold Foiled Inserts, RSVP")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="designs/", blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, help_text="External or CDN image URL")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. New Release, Trending, Bestseller")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    reviews_count = models.IntegerField(default=120)
    is_sale = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_luxe = models.BooleanField(default=False)
    
    tradition = models.CharField(max_length=50, choices=TRADITION_CHOICES, blank=True)
    craft_style = models.CharField(max_length=50, choices=CRAFT_STYLE_CHOICES, blank=True)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="designs",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return ""

    def formatted_price(self):
        return f"₹{self.price:,.2f}"

    def formatted_original_price(self):
        if self.original_price:
            return f"₹{self.original_price:,.2f}"
        return ""

    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            pct = int(round((1 - (float(self.price) / float(self.original_price))) * 100))
            return f"-{pct}%"
        return ""
