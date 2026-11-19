from django.db import migrations

OLD_PRICING_INTRO = (
    "Fixed prices, published before we talk. Every project starts with a "
    "written scope, so the number in the scope is the number on the invoice."
)
NEW_PRICING_INTRO = (
    "Fixed prices, published before we talk. Every project starts with two "
    "documents: an agreement covering who does what and who owns what, and a "
    "statement of work covering scope, price, and dates. The number in the "
    "statement of work is the number on the invoice."
)

WORK_FIELDS = {
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
}

OLD_WORK_FIELDS = {
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
}


def forward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    WorkItem = apps.get_model("home", "WorkItem")
    TeamMember = apps.get_model("home", "TeamMember")

    HomePage.objects.filter(pricing_intro=OLD_PRICING_INTRO).update(
        pricing_intro=NEW_PRICING_INTRO
    )
    WorkItem.objects.filter(client_label__startswith="GrannyCoded").update(
        **WORK_FIELDS
    )
    TeamMember.objects.filter(name="Leah Ballard", role="Designer").update(
        role="Creative director"
    )


def backward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    WorkItem = apps.get_model("home", "WorkItem")
    TeamMember = apps.get_model("home", "TeamMember")

    HomePage.objects.filter(pricing_intro=NEW_PRICING_INTRO).update(
        pricing_intro=OLD_PRICING_INTRO
    )
    WorkItem.objects.filter(client_label__startswith="GrannyCoded").update(
        **OLD_WORK_FIELDS
    )
    TeamMember.objects.filter(name="Leah Ballard", role="Creative director").update(
        role="Designer"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0011_price_note"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
