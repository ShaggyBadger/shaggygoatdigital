"""Create the Sites we've built page and its first project.

Existing pages are refreshed only when explicitly requested.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from home.models import HomePage
from pages.models import PortfolioItem, PortfolioPage

PROJECT = {
    "client_label": "GrannyCoded / Custom storefront",
    "project_title": "One-of-a-kind quilt clothing, sold one piece at a time",
    "problem": (
        "Every piece is a single object: a coat cut from one rescued quilt, a "
        "dress made from a tablecloth. A template store wants forty of the same "
        "thing. She had one of each, and sold them through messages."
    ),
    "built": (
        "A shop built for single items: categories, search, product pages, cart "
        "and checkout, and a custom-order form that arrives with a reference "
        "photo attached. Plus a journal and the policy pages a shop needs."
    ),
    "outcome": (
        "Eleven pieces listed, each sold once. Custom requests come in as a "
        "written brief with a photo, so quoting starts from facts instead of a "
        "back-and-forth."
    ),
    "url": "https://grannycoded.com",
}


class Command(BaseCommand):
    help = "Create the Sites we've built page below the homepage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Repair missing content on an existing page without unpublished edits.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            raise CommandError("No homepage exists to attach the page to.")

        page = (
            PortfolioPage.objects.child_of(home)
            .filter(slug="sites-weve-built")
            .select_for_update()
            .first()
        )
        created = page is None
        if not created:
            if not options["refresh"]:
                self.stdout.write(f"Already exists: {page.url}")
                return
            if page.has_unpublished_changes:
                raise CommandError(f"{page.url} has unpublished changes. Refresh cancelled.")

        if created:
            page = PortfolioPage(
                title="Sites we've built",
                slug="sites-weve-built",
                seo_title="Sites we've built | Shaggy Goat Digital, LLC",
                search_description=(
                    "Live websites built for local businesses in North Carolina, "
                    "with the problem, the build, and what changed."
                ),
            )
            home.add_child(instance=page)

        if not page.items.exists():
            PortfolioItem.objects.create(page=page, sort_order=0, **PROJECT)

        page.save_revision().publish()
        action = "Created" if created else "Refreshed"
        self.stdout.write(self.style.SUCCESS(f"{action} {page.url}"))
