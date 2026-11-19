from django.core.management import call_command
from django.test import TestCase

from pages.models import ContentPage, ProcessPage


class PrivacyPageTests(TestCase):
    def test_seed_command_creates_the_policy_page(self):
        call_command("seed_privacy_page", verbosity=0)

        page = ContentPage.objects.get(slug="privacy")
        self.assertTrue(page.live)

        response = self.client.get("/privacy/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Privacy Policy")
        self.assertContains(response, "Cookies")
        self.assertContains(response, "North Carolina")

    def test_seed_command_is_idempotent(self):
        call_command("seed_privacy_page", verbosity=0)
        call_command("seed_privacy_page", verbosity=0)

        self.assertEqual(ContentPage.objects.filter(slug="privacy").count(), 1)

    def test_footer_links_to_the_policy(self):
        call_command("seed_privacy_page", verbosity=0)

        response = self.client.get("/")

        self.assertContains(response, 'href="/privacy/"')


class ProcessPageTests(TestCase):
    def test_seed_command_adds_the_free_concept_step_once(self):
        call_command("seed_process_page", verbosity=0)
        call_command("seed_process_page", verbosity=0)

        page = ProcessPage.objects.get(slug="how-it-works")
        self.assertEqual(page.steps.count(), 5)
        self.assertEqual(
            page.steps.order_by("sort_order")[1].title,
            "We design the top of your homepage, free.",
        )
        self.assertEqual(page.steps_heading, "Five steps, start to finish")

    def test_page_renders_the_concept_step(self):
        call_command("seed_process_page", verbosity=0)

        response = self.client.get("/how-it-works/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "free")
        self.assertContains(response, "you keep the file")
