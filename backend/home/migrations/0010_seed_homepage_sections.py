from django.db import migrations

PAIN_POINTS = [
    {
        "title": "The words",
        "body": (
            "You write every page. The final draft, in your voice, then a shorter "
            "version for search results. Nobody mentions that the writing is most "
            "of the project."
        ),
    },
    {
        "title": "The photos",
        "body": (
            "Phone photos arrive sideways, then land on a page stretching them "
            "1,400 pixels wide. Somebody says the word optimize and hands you a "
            "tool with fourteen sliders."
        ),
    },
    {
        "title": "The phone screen",
        "body": (
            "It looks fine on your laptop. A customer opens it and the menu is a "
            "wall of tiny links, the form won't scroll, and the map lands across "
            "town."
        ),
    },
    {
        "title": "Getting found",
        "body": (
            "Titles, descriptions, a sitemap, structured data, a Google Business "
            "Profile. None of it is hard. All of it is homework you didn't ask "
            "for."
        ),
    },
]

WORK_ITEMS = [
    {
        "client_label": "GrannyCoded / Custom storefront",
        "project_title": "One-of-a-kind quilt clothing, sold direct",
        "problem": (
            "She sold pieces one at a time through messages. The product photos "
            "existed. A storefront didn't, and neither did a way to add a piece "
            "without calling someone."
        ),
        "built": (
            "A catalog, a checkout, and a content system she runs herself. No "
            "plugin stack, no monthly platform cut."
        ),
        "outcome": "She adds a piece and it appears. She hasn't called us to update it.",
        "url": "https://grannycoded.com",
    },
]

PRICE_TIERS = [
    {
        "name": "Brochure",
        "price": "$500",
        "blurb": "One to three pages that say what you do and make it easy to get in touch.",
        "features": "Up to 3 pages\nContact form\nGoogle setup\nYou edit it yourself",
    },
    {
        "name": "Shop or booking",
        "price": "$1,200",
        "blurb": "A catalog, a checkout, or a booking flow, plus the pages around it.",
        "features": (
            "Everything in Brochure\n"
            "Catalog and checkout, or booking\n"
            "Up to 8 pages\n"
            "Self-editing for products"
        ),
    },
    {
        "name": "Custom",
        "price": "From $2,500",
        "blurb": "Accounts, integrations, or a build that doesn't fit the other two.",
        "features": (
            "Written scope and quote\n"
            "Integrations and custom data\n"
            "Runs two to three months"
        ),
    },
]

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
        "role": "Designer",
        "bio": (
            "Leah handles type, color, spacing, and the small decisions nobody "
            "notices until they're wrong."
        ),
    },
]


def seed_sections(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    PainPoint = apps.get_model("home", "PainPoint")
    WorkItem = apps.get_model("home", "WorkItem")
    PriceTier = apps.get_model("home", "PriceTier")
    TeamMember = apps.get_model("home", "TeamMember")

    page = HomePage.objects.first()
    if page is None:
        return

    if not PainPoint.objects.filter(page_id=page.pk).exists():
        PainPoint.objects.bulk_create(
            [
                PainPoint(page_id=page.pk, sort_order=index, **point)
                for index, point in enumerate(PAIN_POINTS)
            ]
        )

    if not WorkItem.objects.filter(page_id=page.pk).exists():
        WorkItem.objects.bulk_create(
            [
                WorkItem(page_id=page.pk, sort_order=index, **item)
                for index, item in enumerate(WORK_ITEMS)
            ]
        )

    if not PriceTier.objects.filter(page_id=page.pk).exists():
        PriceTier.objects.bulk_create(
            [
                PriceTier(page_id=page.pk, sort_order=index, **tier)
                for index, tier in enumerate(PRICE_TIERS)
            ]
        )

    if not TeamMember.objects.filter(page_id=page.pk).exists():
        TeamMember.objects.bulk_create(
            [
                TeamMember(page_id=page.pk, sort_order=index, **member)
                for index, member in enumerate(TEAM)
            ]
        )


def unseed_sections(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    page = HomePage.objects.first()
    if page is None:
        return

    for model_name in ("PainPoint", "WorkItem", "PriceTier", "TeamMember"):
        model = apps.get_model("home", model_name)
        model.objects.filter(page_id=page.pk).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0009_remove_homepage_pricing_amount_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_sections, unseed_sections),
    ]
