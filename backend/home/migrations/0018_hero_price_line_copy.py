from django.db import migrations


def forward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    for page in HomePage.objects.filter(hero_price_line__contains="Brochure sites from"):
        page.hero_price_line = page.hero_price_line.replace(
            "Brochure sites from", "Starter sites from"
        )
        page.save(update_fields=["hero_price_line"])


def backward(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    for page in HomePage.objects.filter(hero_price_line__contains="Starter sites from"):
        page.hero_price_line = page.hero_price_line.replace(
            "Starter sites from", "Brochure sites from"
        )
        page.save(update_fields=["hero_price_line"])


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0017_alter_contactsubmission_need_and_more"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
