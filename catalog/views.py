import urllib.parse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.conf import settings
from .models import Design, Category


def get_whatsapp_number():
    return getattr(settings, "WHATSAPP_NUMBER", "919618022264")


def home(request):
    """Homepage with luxury hero, new arrivals, budget categories, and testimonials."""
    categories = Category.objects.all()
    designs = Design.objects.select_related("category").all()
    
    new_arrivals = designs.filter(is_new=True)
    if not new_arrivals.exists():
        new_arrivals = designs[:3]

    context = {
        "categories": categories,
        "new_arrivals": new_arrivals,
        "designs": designs[:6],
        "whatsapp_number": get_whatsapp_number(),
    }
    return render(request, "catalog/home.html", context)


def all_invitations(request):
    """All invitations collection page showing all designs with optional search query."""
    categories = Category.objects.all()
    designs = Design.objects.select_related("category").all()

    # Search query
    q = request.GET.get("q", "").strip()
    if q:
        designs = designs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(sku__icontains=q) |
            Q(subtitle__icontains=q)
        )

    context = {
        "categories": categories,
        "designs": designs,
        "total_count": designs.count(),
        "search_query": q,
        "whatsapp_number": get_whatsapp_number(),
    }
    return render(request, "catalog/all_invitations.html", context)


def contact_us(request):
    """Contact Us & Wedding WhatsApp page."""
    submitted = False
    if request.method == "POST":
        submitted = True

    context = {
        "submitted": submitted,
        "whatsapp_number": get_whatsapp_number(),
    }
    return render(request, "catalog/contact_us.html", context)


def design_detail(request, pk):
    """Detailed page for inspecting a single wedding card design with WhatsApp direct inquiry."""
    design = get_object_or_404(Design, pk=pk)
    whatsapp_num = get_whatsapp_number()

    message = (
        f"Hello! I am interested in the wedding card design:\n"
        f"• Name: {design.name}\n"
        f"• SKU: {design.sku}\n"
        f"• Price: {design.formatted_price()}\n"
        f"Could you please share details on paper customization, sample delivery, and printing time?"
    )
    whatsapp_url = f"https://wa.me/{whatsapp_num}?text={urllib.parse.quote(message)}"

    related_designs = Design.objects.exclude(pk=design.pk)
    if design.category:
        related_designs = related_designs.filter(category=design.category)
    related_designs = related_designs[:4]

    context = {
        "design": design,
        "whatsapp_url": whatsapp_url,
        "related_designs": related_designs,
        "whatsapp_number": whatsapp_num,
    }
    return render(request, "catalog/design_detail.html", context)
