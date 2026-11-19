from django.db import migrations

OLD_NOTE = "We put it in writing first. We're stubborn that way."
NEW_NOTE = "Maintenance is $50 a month: updates, backups, and small changes. Cancel whenever."


def update_price_note(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    HomePage.objects.filter(pricing_note=OLD_NOTE).update(pricing_note=NEW_NOTE)


def restore_price_note(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    HomePage.objects.filter(pricing_note=NEW_NOTE).update(pricing_note=OLD_NOTE)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0010_seed_homepage_sections"),
    ]

    operations = [
        migrations.RunPython(update_price_note, restore_price_note),
    ]
