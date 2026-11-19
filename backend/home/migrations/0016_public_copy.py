from django.db import migrations

OLD_PRICE_LINE = "<p>Brochure sites from <strong>$500</strong>. Maintenance <strong>$50 a month</strong>. Custom work quoted after we talk.</p>"
NEW_PRICE_LINE = "<p>Starter sites from <strong>$500</strong>. Maintenance <strong>$50 a month</strong>. Custom work quoted after we talk.</p>"

OLD_FOOTNOTE = (
    "If two of those sound like your week, start with a brochure site. "
    "We'll tell you when you need the rest."
)
NEW_FOOTNOTE = (
    "If two of those sound like your week, start small and grow into the rest. "
    "We'll tell you when you actually need it."
)

OLD_DESCRIPTION = (
    "Shaggy Goat Digital, LLC builds sharp, fast websites for local businesses, "
    "then keeps them running. Brochure sites from $500."
)
NEW_DESCRIPTION = (
    "Shaggy Goat Digital, LLC builds sharp, fast websites for local businesses in "
    "North Carolina, then keeps them running. Starter sites from $500."
)


def forward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    HomePage.objects.filter(
        hero_price_line=OLD_PRICE_LINE
    ).update(hero_price_line=NEW_PRICE_LINE)
    HomePage.objects.filter(
        services_footnote=OLD_FOOTNOTE
    ).update(services_footnote=NEW_FOOTNOTE)
    HomePage.objects.filter(
        search_description=OLD_DESCRIPTION
    ).update(search_description=NEW_DESCRIPTION)


def backward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    HomePage.objects.filter(
        hero_price_line=NEW_PRICE_LINE
    ).update(hero_price_line=OLD_PRICE_LINE)
    HomePage.objects.filter(
        services_footnote=NEW_FOOTNOTE
    ).update(services_footnote=OLD_FOOTNOTE)
    HomePage.objects.filter(
        search_description=NEW_DESCRIPTION
    ).update(search_description=OLD_DESCRIPTION)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0015_tier_copy"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
