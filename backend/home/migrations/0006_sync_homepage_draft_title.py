from django.db import migrations


def sync_draft_title(apps, schema_editor):
    """Keep the admin title in sync after the initial page conversion."""
    HomePage = apps.get_model("home", "HomePage")

    page = HomePage.objects.first()
    if page is None:
        return

    if (
        page.title == "Shaggy Goat Digital"
        and page.draft_title == "Welcome to your new Wagtail site!"
    ):
        page.draft_title = "Shaggy Goat Digital"
        page.save(update_fields=["draft_title"])


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_homepage_footer_tagline_homepage_nav_cta_label_and_more"),
    ]

    operations = [
        migrations.RunPython(sync_draft_title, migrations.RunPython.noop),
    ]
