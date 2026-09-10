from django.conf import settings


def whatsapp_number(request):
    """Inject WHATSAPP_NUMBER into every template context."""
    return {"WHATSAPP_NUMBER": getattr(settings, "WHATSAPP_NUMBER", "919618022264")}
