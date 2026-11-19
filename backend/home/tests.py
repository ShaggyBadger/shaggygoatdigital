from django.core import mail
from django.test import TestCase, override_settings
from wagtail.models import Site

from .models import ContactSubmission, HomePage


class HomePageTests(TestCase):
    def setUp(self):
        self.page = Site.objects.get(is_default_site=True).root_page.specific
        self.assertIsInstance(self.page, HomePage)
        self.form_data = {
            "name": "Dana Reed",
            "email": "dana@example.com",
            "business": "Reed Electric",
            "need": "brochure",
            "message": "We need a real site and a booking form.",
        }

    def test_home_page_renders_approved_copy(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Shaggy Goat Digital, LLC | Websites with a backbone</title>")
        self.assertContains(response, "Websites with a backbone.")
        self.assertContains(response, "You could build this yourself.")
        self.assertContains(response, "Getting found")
        self.assertContains(response, "Get found")
        self.assertContains(response, "GrannyCoded")
        self.assertContains(response, "Visit the site")
        self.assertContains(response, "Brochure")
        self.assertContains(response, "From $2,500")
        self.assertContains(response, "Maintenance is $50 a month")
        self.assertContains(response, "Testimonials")
        self.assertContains(response, "I sent over product photos")
        self.assertContains(response, "Josh Ballard")
        self.assertContains(response, "Leah Ballard")
        self.assertContains(response, "Creative director")
        self.assertContains(response, "statement of work")
        self.assertContains(response, "North Carolina")
        self.assertContains(response, "No scapegoats.")
        self.assertContains(response, 'itemtype="https://schema.org/Review"')
        self.assertContains(response, '"@type": "Organization"')
        self.assertContains(response, '"addressRegion": "NC"')
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'href="/#testimonials"')
        self.assertContains(response, 'href="/#work"')

    def test_seed_creates_three_service_cards(self):
        self.assertEqual(self.page.service_cards.count(), 3)

    def test_seed_creates_sales_sections(self):
        self.assertEqual(self.page.pain_points.count(), 4)
        self.assertEqual(self.page.work_items.count(), 1)
        self.assertEqual(self.page.price_tiers.count(), 3)
        self.assertEqual(self.page.team_members.count(), 2)

    def test_contact_submission_is_saved(self):
        response = self.client.post("/", self.form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Got it. We")
        submission = ContactSubmission.objects.get()
        self.assertEqual(submission.name, "Dana Reed")
        self.assertEqual(submission.email, "dana@example.com")
        self.assertEqual(submission.need, "brochure")

    def test_invalid_email_is_rejected(self):
        data = {**self.form_data, "email": "not-an-email"}

        response = self.client.post("/", data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check the form and try again.")
        self.assertEqual(ContactSubmission.objects.count(), 0)

    def test_honeypot_submission_is_ignored(self):
        data = {**self.form_data, "website": "https://spam.example"}

        self.client.post("/", data)

        self.assertEqual(ContactSubmission.objects.count(), 0)

    @override_settings(
        CONTACT_EMAIL="owner@example.com",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_notification_email_is_sent(self):
        self.client.post("/", self.form_data)

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ["owner@example.com"])
        self.assertIn("Dana Reed", message.subject)
        self.assertIn("Reed Electric", message.body)

    @override_settings(CONTACT_EMAIL="")
    def test_notification_is_skipped_without_address(self):
        self.client.post("/", self.form_data)

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(ContactSubmission.objects.count(), 1)


class ContactSubmissionAdminTests(TestCase):
    def test_submission_admin_requires_login_and_renders(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser(
            "admin", "admin@example.com", "test-password"
        )
        self.client.force_login(user)

        response = self.client.get("/admin/contactsubmission/")

        self.assertEqual(response.status_code, 200)


class HomePageAdminTests(TestCase):
    def test_admin_login_shows_goat_branding(self):
        response = self.client.get("/admin/login/")

        self.assertContains(response, "Sign in to Shaggy Goat Digital")
        self.assertContains(response, 'viewBox="120 20 260 265"')
        self.assertContains(response, "brand/shaggy-goat-icon.svg")
        self.assertContains(response, "wagtailadmin/css/goat-branding.css")

    def test_home_page_edit_view_renders(self):
        from django.contrib.auth import get_user_model
        from wagtail.models import Site

        user = get_user_model().objects.create_superuser(
            "editor", "editor@example.com", "test-password"
        )
        self.client.force_login(user)
        page = Site.objects.get(is_default_site=True).root_page

        response = self.client.get(f"/admin/pages/{page.pk}/edit/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'viewBox="120 20 260 265"')
        self.assertContains(response, f'href="/admin/pages/{page.pk}/edit/"')
