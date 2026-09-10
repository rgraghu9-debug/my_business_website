from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("all-invitations/", views.all_invitations, name="all_invitations"),
    path("contact-us/", views.contact_us, name="contact_us"),
    path("design/<int:pk>/", views.design_detail, name="design_detail"),
]
