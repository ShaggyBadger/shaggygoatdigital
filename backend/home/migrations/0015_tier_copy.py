from django.db import migrations

OLD_PAIN_INTRO = (
    "Anyone can. Wix, Squarespace, and a weekend will get you a site. What that "
    "weekend actually costs is the part nobody mentions."
)
NEW_PAIN_INTRO = "Anyone can. Wix, Squarespace, and a weekend will get you a site."

OLD_PAIN_FOOTNOTE = (
    "That's the job. We do it, and you get a site that works in a customer's hand."
)
NEW_PAIN_FOOTNOTE = (
    "A goat can climb a wall. You still wouldn't hire it to build the house."
)

TIERS = {
    "Brochure": {
        "name": "Starter site",
        "price": "$500",
        "blurb": (
            "The site a local business actually needs: what you do, where you "
            "work, and how to reach you."
        ),
        "features": (
            "A site you can update yourself\n"
            "Contact form and click-to-call\n"
            "Google setup"
        ),
    },
    "Shop or booking": {
        "name": "Sell or book",
        "price": "$1,200",
        "blurb": (
            "A catalog and checkout, or a booking flow, plus the pages around it."
        ),
        "features": (
            "Everything in Starter\n"
            "Catalog and checkout, or booking\n"
            "Add products or bookings yourself"
        ),
    },
    "Custom": {
        "name": "Custom build",
        "price": "From $2,500",
        "blurb": "Accounts, integrations, or a build that doesn't fit the other two.",
        "features": (
            "Written scope and quote\n"
            "Integrations and custom data\n"
            "Runs two to three months"
        ),
    },
}

OLD_TIERS = {
    "Starter site": {"name": "Brochure", "price": "$500"},
    "Sell or book": {"name": "Shop or booking", "price": "$1,200"},
    "Custom build": {"name": "Custom", "price": "From $2,500"},
}


def forward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    PriceTier = apps.get_model("home", "PriceTier")

    HomePage.objects.filter(pain_intro=OLD_PAIN_INTRO).update(pain_intro=NEW_PAIN_INTRO)
    HomePage.objects.filter(pain_footnote=OLD_PAIN_FOOTNOTE).update(
        pain_footnote=NEW_PAIN_FOOTNOTE
    )

    for old_name, values in TIERS.items():
        PriceTier.objects.filter(name=old_name).update(**values)


def backward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    PriceTier = apps.get_model("home", "PriceTier")

    HomePage.objects.filter(pain_intro=NEW_PAIN_INTRO).update(pain_intro=OLD_PAIN_INTRO)
    HomePage.objects.filter(pain_footnote=NEW_PAIN_FOOTNOTE).update(
        pain_footnote=OLD_PAIN_FOOTNOTE
    )

    for new_name, values in OLD_TIERS.items():
        PriceTier.objects.filter(name=new_name).update(**values)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0014_remove_workitem_image_remove_workitem_page_and_more"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
