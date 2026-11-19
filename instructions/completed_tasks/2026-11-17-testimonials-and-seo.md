# Testimonials section and SEO

## Goal

Replace the portfolio section with a testimonial section, keep the copy editable
in Wagtail, and add accurate on-page metadata and structured data.

## Steps

- Rename the portfolio model fields to testimonial fields, remove the unused
  project summary and portfolio CTA, and migrate the existing seeded values.
- Render one semantic testimonial with `Review` microdata.
- Add canonical, Open Graph, and Twitter metadata plus `Organization` JSON-LD.
- Update the nav/footer links from Portfolio to Testimonials.
- Add regression assertions for the section copy, Review markup, and SEO tags.
- Verify the desktop and mobile layouts.

## Verification

```bash
docker compose exec web python manage.py makemigrations --check
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec tailwind npm run build:css
```

## Completion summary

- Renamed the portfolio fields to testimonial fields and removed the unused
  project summary and portfolio CTA (migration `0008`).
- Replaced the portfolio block with a semantic testimonial using `Review`
  microdata, a large quote, client label, and attribution.
- Updated navigation and footer links to `#testimonials`.
- Added canonical, Open Graph, Twitter, and `Organization` JSON-LD metadata.
  The document title now uses Wagtail's SEO title.
- Added `sitemap.xml` through Wagtail sitemaps and a `robots.txt` that points at
  it and excludes the admin.
- Added the `absolute_url` filter so local and object-storage image URLs both
  work in social metadata.
- Tests cover the section copy, Review markup, canonical tag, and nav link.

Checks run:

```bash
docker compose exec web python manage.py makemigrations --check
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check
docker compose exec web python manage.py test       # 10 passed
docker compose exec tailwind npm run build:css
```

Follow-ups:

- Replace the placeholder testimonial with the real review.
- Set the Wagtail Site hostname to the production domain so the sitemap uses it.
- Add a testimonials page and link to it only when there is more than one.
