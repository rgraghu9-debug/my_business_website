from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Category, Design


class CategoryModelTest(TestCase):
    def test_category_creation_and_slug(self):
        category = Category.objects.create(name="Hindu Wedding Cards")
        self.assertEqual(category.slug, "hindu-wedding-cards")
        self.assertEqual(str(category), "Hindu Wedding Cards")


class DesignModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Royal Collections")
        self.design = Design.objects.create(
            name="Rotating Wheel Shubh Muhurat Card",
            subtitle="Interactive Mechanism & 3 Inserts",
            description="Luxury card with gold foil details.",
            price=310.00,
            original_price=360.00,
            sku="SV-124",
            badge="Bestseller",
            rating=4.9,
            reviews_count=85,
            is_new=True,
            is_luxe=True,
            category=self.category,
            image_url="https://example.com/sample.jpg"
        )

    def test_design_formatted_price(self):
        self.assertEqual(self.design.formatted_price(), "₹310.00")

    def test_design_original_price(self):
        self.assertEqual(self.design.formatted_original_price(), "₹360.00")

    def test_design_discount_percent(self):
        # 360 -> 310 is a ~14% discount
        self.assertEqual(self.design.discount_percent(), "-14%")

    def test_design_get_image_url(self):
        self.assertEqual(self.design.get_image_url(), "https://example.com/sample.jpg")


class StorefrontViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Storefront Category")
        self.design = Design.objects.create(
            name="Gold Foil Peacock Card",
            price=250.00,
            sku="SV-101",
            category=self.category,
            is_new=True
        )

    def test_home_page_status_code_and_template(self):
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/home.html")
        self.assertIn("categories", response.context)
        self.assertIn("whatsapp_number", response.context)

    def test_all_invitations_page_status_code(self):
        response = self.client.get(reverse("catalog:all_invitations"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/all_invitations.html")
        self.assertEqual(response.context["total_count"], 1)

    def test_all_invitations_search_filter(self):
        response = self.client.get(reverse("catalog:all_invitations") + "?q=Peacock")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_count"], 1)

        response_no_match = self.client.get(reverse("catalog:all_invitations") + "?q=NonExistentCard")
        self.assertEqual(response_no_match.context["total_count"], 0)

    def test_contact_us_page_get_and_post(self):
        response_get = self.client.get(reverse("catalog:contact_us"))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "catalog/contact_us.html")

        response_post = self.client.post(reverse("catalog:contact_us"), {
            "name": "Ananya Sharma",
            "phone": "9876543210",
            "message": "Interested in sample kit."
        })
        self.assertEqual(response_post.status_code, 200)
        self.assertTrue(response_post.context["submitted"])

    def test_design_detail_page_and_whatsapp_url(self):
        response = self.client.get(reverse("catalog:design_detail", kwargs={"pk": self.design.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/design_detail.html")
        self.assertIn("whatsapp_url", response.context)
        self.assertIn("SV-101", response.context["whatsapp_url"])

    def test_design_detail_404(self):
        response = self.client.get(reverse("catalog:design_detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)


class AdminViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.admin_user = User.objects.create_superuser(
            username="admin_tester",
            email="admin@test.com",
            password="testpassword123"
        )

    def test_admin_login_and_dashboard_access(self):
        # Access login page
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 200)

        # Perform login
        login_success = self.client.login(username="admin_tester", password="testpassword123")
        self.assertTrue(login_success)

        # Access admin index
        index_response = self.client.get(reverse("admin:index"))
        self.assertEqual(index_response.status_code, 200)

        # Access catalog design changelist
        changelist_response = self.client.get("/admin/catalog/design/")
        self.assertEqual(changelist_response.status_code, 200)
