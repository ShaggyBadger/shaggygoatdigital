from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from pages.models import AboutPage, ContentPage, PortfolioPage, ProcessPage


class PrivacyPageTests(TestCase):
    def test_seed_command_creates_the_policy_page(self):
        call_command("seed_privacy_page", verbosity=0)

        page = ContentPage.objects.get(slug="privacy")
        self.assertTrue(page.live)

        response = self.client.get("/privacy/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Privacy Policy")
        self.assertContains(response, "Your email address, phone number, or both")
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
        self.assertContains(response, "What you own")
        self.assertNotContains(response, "Who this isn")
        self.assertContains(
            response,
            '<a href="/#contact" class="underline">You: fill in the form. Two minutes.</a>',
            count=1,
            html=True,
        )


class PortfolioPageTests(TestCase):
    def test_seed_command_creates_the_page_and_project(self):
        call_command("seed_portfolio_page", verbosity=0)
        call_command("seed_portfolio_page", verbosity=0)

        page = PortfolioPage.objects.get(slug="sites-weve-built")
        self.assertEqual(page.items.count(), 1)

        response = self.client.get("/sites-weve-built/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GrannyCoded")
        self.assertContains(response, "Visit the site")

    def test_homepage_links_to_the_page(self):
        call_command("seed_portfolio_page", verbosity=0)

        response = self.client.get("/")

        self.assertContains(response, 'href="/sites-weve-built/"', count=4)


class SeedRefreshTests(TestCase):
    def test_reseeding_preserves_live_pages_and_unpublished_drafts(self):
        for command, page_type, child_relation, child_title, count in (
            ("seed_process_page", ProcessPage, "steps", "title", 5),
            ("seed_portfolio_page", PortfolioPage, "items", "project_title", 1),
        ):
            with self.subTest(command=command):
                call_command(command, verbosity=0)
                page = page_type.objects.get()
                self.assertTrue(page.live)
                self.assertEqual(getattr(page, child_relation).count(), count)
                live_revision_id = page.latest_revision_id
                live_title = page.title
                children = list(getattr(page, child_relation).all())
                live_child_title = getattr(children[0], child_title)

                call_command(command, verbosity=0)
                page = page_type.objects.get(pk=page.pk)
                self.assertEqual(page.latest_revision_id, live_revision_id)
                self.assertEqual(page.revisions.count(), 1)
                self.assertEqual(getattr(page, child_relation).count(), count)

                page.title = "Draft title"
                setattr(children[0], child_title, "Draft child title")
                getattr(page, child_relation).set(children)
                draft = page.save_revision()

                call_command(command, verbosity=0)
                with self.assertRaisesMessage(CommandError, "has unpublished changes"):
                    call_command(command, refresh=True, verbosity=0)

                page = page_type.objects.get(pk=page.pk)
                self.assertEqual(page.latest_revision_id, draft.pk)
                self.assertEqual(page.live_revision_id, live_revision_id)
                self.assertEqual(page.revisions.count(), 2)
                self.assertEqual(page.title, live_title)
                self.assertEqual(
                    getattr(getattr(page, child_relation).first(), child_title),
                    live_child_title,
                )
                self.assertTrue(page.has_unpublished_changes)
                draft.refresh_from_db()
                draft_page = draft.as_object()
                self.assertEqual(draft_page.title, "Draft title")
                self.assertEqual(
                    getattr(getattr(draft_page, child_relation).first(), child_title),
                    "Draft child title",
                )

    def test_refresh_repairs_legacy_process_steps(self):
        call_command("seed_process_page", verbosity=0)
        page = ProcessPage.objects.get()
        steps = list(page.steps.order_by("sort_order"))
        concept_title = steps.pop(1).title
        for index, step in enumerate(steps):
            step.sort_order = index
        page.steps.set(steps)
        page.steps_heading = "Four steps, start to finish"
        page.save_revision().publish()

        call_command("seed_process_page", refresh=True, verbosity=0)
        call_command("seed_process_page", refresh=True, verbosity=0)
        page = ProcessPage.objects.get(pk=page.pk)
        self.assertEqual(page.steps_heading, "Five steps, start to finish")
        self.assertEqual(page.steps.count(), 5)
        self.assertEqual(page.steps.order_by("sort_order")[1].title, concept_title)

    def test_refresh_repairs_missing_portfolio_item(self):
        call_command("seed_portfolio_page", verbosity=0)
        page = PortfolioPage.objects.get()
        page.items.set([])
        page.save_revision().publish()

        call_command("seed_portfolio_page", refresh=True, verbosity=0)
        call_command("seed_portfolio_page", refresh=True, verbosity=0)
        page = PortfolioPage.objects.get(pk=page.pk)
        self.assertEqual(page.items.count(), 1)


class AboutPageTests(TestCase):
    def test_seed_command_creates_the_page_and_team(self):
        call_command("seed_about_page", verbosity=0)
        call_command("seed_about_page", verbosity=0)

        page = AboutPage.objects.get(slug="about")
        self.assertEqual(page.team_members.count(), 2)

        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Why we started")
        self.assertContains(response, "Josh Ballard")
        self.assertContains(response, "Creative director")
        self.assertContains(response, "North Carolina")

    def test_homepage_no_longer_carries_the_team(self):
        call_command("seed_about_page", verbosity=0)

        response = self.client.get("/")

        self.assertNotContains(response, "Leah Ballard")
        self.assertContains(response, 'href="/about/"', count=3)
