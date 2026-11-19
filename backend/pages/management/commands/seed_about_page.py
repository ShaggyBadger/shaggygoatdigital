"""Create the About page, with the story and the two people behind it.

Idempotent: re-running only fills missing rows, so admin edits survive.
"""

from django.core.management.base import BaseCommand, CommandError

from home.models import HomePage
from pages.models import AboutPage, TeamMember

TEAM = [
    {
        "name": "Josh Ballard",
        "role": "Build and development",
        "bio": (
            "Josh writes the code, sets up the server, and answers the phone when "
            "something breaks at the wrong time."
        ),
    },
    {
        "name": "Leah Ballard",
        "role": "Creative director",
        "bio": (
            "Leah handles type, color, spacing, and the small decisions nobody "
            "notices until they're wrong."
        ),
    },
]


class Command(BaseCommand):
    help = "Create the About page below the homepage."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            raise CommandError("No homepage exists to attach the page to.")

        page = AboutPage.objects.child_of(home).filter(slug="about").first()
        created = page is None

        if created:
            page = AboutPage(
                title="About",
                slug="about",
                seo_title="About | Shaggy Goat Digital, LLC",
                search_description=(
                    "Two people in North Carolina building small, fast websites "
                    "for local businesses, and the reason we started."
                ),
            )
            home.add_child(instance=page)

        if not page.team_members.exists():
            for index, member in enumerate(TEAM):
                TeamMember.objects.create(page=page, sort_order=index, **member)

        page.save_revision().publish()
        action = "Created" if created else "Refreshed"
        self.stdout.write(self.style.SUCCESS(f"{action} {page.url}"))
