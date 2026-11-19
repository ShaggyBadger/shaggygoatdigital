"""Create the How-it-works page below the homepage.

Idempotent: running it again only fills in missing rows and republishes, so it
is safe after a content edit in the Wagtail admin.
"""

from django.core.management.base import BaseCommand, CommandError

from home.models import HomePage
from pages.models import FaqItem, ProcessPage, ProcessStep, StackItem

STEPS = [
    {
        "title": "You tell us what you're running.",
        "body": (
            "One sentence is enough: what the business does, who it serves, and "
            "what the site has to do. Show up in search, take bookings, or sell "
            "things. If you have a logo and photos, send them along. If you "
            "don't, we build around what's there."
        ),
        "client_note": "You: fill in the form. Two minutes.",
    },
    {
        "title": "We design the top of your homepage, free.",
        "body": (
            "Before you pay anything, we design the first screen of your site: "
            "the headline, the layout, and how it looks on a phone. You see the "
            "direction while it can still change. If it's wrong, you owe nothing "
            "and you keep the file."
        ),
        "client_note": "You: look at it and say what's off.",
    },
    {
        "title": "We quote it in writing.",
        "body": (
            "A fixed price for the pages you asked for, plus a plain list of "
            "what isn't in it. Usually back within two business days. If the job "
            "and the budget don't line up, you hear that on the first call "
            "instead of the third."
        ),
        "client_note": "You: read it, ask questions, approve it.",
    },
    {
        "title": "We build it.",
        "body": (
            "Two to three weeks for a brochure site. You get a staging link on "
            "day one that opens on your phone, so nothing is a surprise at the "
            "end. Words, photos, and page structure get settled before anything "
            "is styled."
        ),
        "client_note": "You: send content. Check the link.",
    },
    {
        "title": "It goes live and stays up.",
        "body": (
            "We point the domain, check every form and payment, and hand over "
            "the keys. Maintenance covers framework and server updates, backups, "
            "and small changes for $50 a month."
        ),
        "client_note": "You: nothing, unless something breaks.",
    },
]

STACK = [
    ("Framework", "Django, with Wagtail as the editor you'll actually use."),
    ("Database", "PostgreSQL. Content is stored and backed up, not baked into pages."),
    ("Styling", "Tailwind, compiled to one stylesheet. Pages are HTML first."),
    ("Hosting", "A dedicated server, not a shared plan with a thousand neighbours."),
    ("Images", "Object storage, resized per screen, so phones pull phone-sized photos."),
    ("Weight", "Pages arrive as HTML and one stylesheet, before any script finishes."),
]

FAQ = [
    (
        "How long does a site take?",
        "Two to three weeks for a brochure site, counted from the day your "
        "content lands. A shop or a booking flow runs four to six.",
    ),
    (
        "Can I edit it myself?",
        "Yes. Everything on this page is editable in the admin, including this "
        "answer. If you'd rather not touch it, the monthly plan covers small "
        "changes.",
    ),
    (
        "What happens to my old site?",
        "We keep the domain, move the content worth keeping, and set redirects "
        "so links people already have still land somewhere sensible.",
    ),
    (
        "Do you do SEO?",
        "The technical half: fast pages, real headings, clean titles, a sitemap, "
        "and content that renders without JavaScript. We don't sell rankings by "
        "the month and we won't promise a position on Google.",
    ),
    (
        "What does $50 a month cover?",
        "Framework and server updates, backups, uptime checks, and small "
        "changes. Bigger work gets quoted first.",
    ),
    (
        "Who's the goat?",
        "Josh Ballard, mostly. The goat is the mascot because goats climb what "
        "they shouldn't and don't fall off.",
    ),
]


class Command(BaseCommand):
    help = "Create or refresh the How-it-works page below the homepage."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            raise CommandError("No homepage exists to attach the page to.")

        page = ProcessPage.objects.child_of(home).first()
        created = page is None
        if created:
            page = ProcessPage(
                title="How this works",
                slug="how-it-works",
                seo_title="How it works | Shaggy Goat Digital, LLC",
                search_description=(
                    "The five steps from an email to a live site, what's under "
                    "the hood, what you own afterwards, and what $50 a month of "
                    "maintenance covers."
                ),
            )
            home.add_child(instance=page)

        if not page.steps.exists():
            ProcessStep.objects.bulk_create(
                [
                    ProcessStep(page=page, sort_order=index, **step)
                    for index, step in enumerate(STEPS)
                ]
            )
        elif not page.steps.filter(title=STEPS[1]["title"]).exists():
            # Existing pages predate the free-concept step: shift the steps that
            # follow it down one place, then insert at position two.
            for step in page.steps.filter(sort_order__gte=1).order_by("-sort_order"):
                step.sort_order += 1
                step.save(update_fields=["sort_order"])
            ProcessStep.objects.create(page=page, sort_order=1, **STEPS[1])

        if page.steps_heading == "Four steps, start to finish":
            page.steps_heading = "Five steps, start to finish"
        if page.steps_intro.startswith("Most of these take a day or two. You handle the first"):
            page.steps_intro = (
                "Most of these take a day or two. You handle the first one and "
                "the fourth one. We do the rest."
            )
        if page.intro.startswith("Four steps from one sentence"):
            page.intro = (
                "Five steps from one sentence in a form to a site you can send "
                "people to. Here is the whole thing, in order, including the "
                "parts that usually get left until after the invoice."
            )

        if not page.stack_items.exists():
            StackItem.objects.bulk_create(
                [
                    StackItem(page=page, sort_order=index, label=label, value=value)
                    for index, (label, value) in enumerate(STACK)
                ]
            )

        if not page.faq_items.exists():
            FaqItem.objects.bulk_create(
                [
                    FaqItem(page=page, sort_order=index, question=question, answer=answer)
                    for index, (question, answer) in enumerate(FAQ)
                ]
            )

        page.save_revision().publish()
        action = "Created" if created else "Refreshed"
        self.stdout.write(self.style.SUCCESS(f"{action} {page.url}"))
