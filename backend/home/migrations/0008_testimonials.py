from django.db import migrations, models

LONG_QUOTE = (
    "I sent over product photos and a rough idea of what I wanted. What came "
    "back looked like the business I'd been trying to explain for years. I can "
    "add a piece now without calling anyone."
)


def update_testimonial_copy(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    page = HomePage.objects.first()
    if page is None:
        return

    changed = []
    if page.testimonials_heading == "Portfolio":
        page.testimonials_heading = "Testimonials"
        changed.append("testimonials_heading")
    if page.testimonials_intro.startswith("A custom storefront"):
        page.testimonials_intro = "What it's like to work with us."
        changed.append("testimonials_intro")
    if page.testimonial_quote == "I can add a piece without calling anyone.":
        page.testimonial_quote = LONG_QUOTE
        changed.append("testimonial_quote")

    if changed:
        page.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_alter_homepage_portfolio_url"),
    ]

    operations = [
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_heading",
            new_name="testimonials_heading",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_intro",
            new_name="testimonials_intro",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_project_label",
            new_name="testimonial_client_label",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_quote",
            new_name="testimonial_quote",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_quote_author",
            new_name="testimonial_author",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_quote_company",
            new_name="testimonial_company",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="portfolio_quote_url",
            new_name="testimonial_company_url",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="portfolio_project_summary",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="portfolio_cta_label",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="portfolio_url",
        ),
        migrations.AlterField(
            model_name="homepage",
            name="testimonials_heading",
            field=models.CharField(default="Testimonials", max_length=80),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="testimonials_intro",
            field=models.CharField(
                default="What it's like to work with us.",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="testimonial_quote",
            field=models.TextField(default=LONG_QUOTE),
        ),
        migrations.RunPython(update_testimonial_copy, migrations.RunPython.noop),
    ]
