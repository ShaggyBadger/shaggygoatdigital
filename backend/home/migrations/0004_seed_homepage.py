from django.db import migrations

SERVICE_CARDS = [
    {
        "title": "Get found",
        "description": "A clean site that shows up when someone searches your name.",
        "price_label": "From $500",
    },
    {
        "title": "Sell or book",
        "description": (
            "Catalog, checkout, scheduling, or payments. Built around how you work."
        ),
        "price_label": "Quoted after we talk",
    },
    {
        "title": "Stay running",
        "description": "Updates, backups, and small changes without a ticket queue.",
        "price_label": "$50 a month",
    },
]


def seed_homepage(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    ServiceCard = apps.get_model("home", "ServiceCard")

    page = HomePage.objects.first()
    if page is None:
        return

    if page.title == "Welcome to your new Wagtail site!":
        page.title = "Shaggy Goat Digital"
        page.draft_title = "Shaggy Goat Digital"
        page.seo_title = "Shaggy Goat Digital, LLC | Websites with a backbone"
        page.search_description = (
            "Shaggy Goat Digital, LLC builds sharp, fast websites for local "
            "businesses, then keeps them running. Brochure sites from $500."
        )
        page.save(
            update_fields=["title", "draft_title", "seo_title", "search_description"]
        )

    if not ServiceCard.objects.filter(page_id=page.pk).exists():
        ServiceCard.objects.bulk_create(
            [
                ServiceCard(page_id=page.pk, sort_order=index, **card)
                for index, card in enumerate(SERVICE_CARDS)
            ]
        )


def unseed_homepage(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    ServiceCard = apps.get_model("home", "ServiceCard")

    page = HomePage.objects.first()
    if page is not None:
        ServiceCard.objects.filter(page_id=page.pk).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_contactsubmission_remove_homepage_intro_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_homepage, unseed_homepage),
    ]
