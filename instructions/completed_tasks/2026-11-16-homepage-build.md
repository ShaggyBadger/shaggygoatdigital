# Homepage build

## Goal

Build the approved Shaggy Goat Digital homepage in Wagtail so every piece of copy,
the service cards, and the hero image are editable in the admin, and so the
contact form saves submissions and sends a notification.

## Approach

- Keep the fixed one-page section order from the demo.
- Store page copy in named `HomePage` fields grouped into admin panels.
- Store the three service cards in an orderable child model.
- Add a `ContactSubmission` model, a Django form, and a `HomePage.serve`
  POST handler.
- Send a notification email through Django's email backend. Development uses
  the console backend; production SMTP is environment-configured.
- Port the approved demo CSS into the Tailwind entry point and let Tailwind
  build `backend/static/css/site.css`.
- Seed the approved copy and service cards in a data migration.
- Use a Wagtail image field for the hero, with a dark gradient fallback when no
  image is uploaded.

## Files

- `backend/home/models.py`
- `backend/home/forms.py`
- `backend/home/wagtail_hooks.py`
- `backend/home/templates/home/home_page.html`
- `backend/templates/base.html`
- `backend/templates/partials/site_nav.html`
- `backend/templates/partials/site_footer.html`
- `backend/static-src/css/input.css`
- `backend/config/settings.py`
- `.env.example`
- `backend/home/migrations/`
- `backend/home/tests.py`

## Seed copy

The approved homepage copy, including the goat humor, "No scapegoats," and the
portfolio testimonial placeholder.

## Verification

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec tailwind npm run build:css
```

Also capture desktop and mobile screenshots of the running page and exercise the
contact form.

## Completion summary

Built the approved homepage in Wagtail.

- Every section's copy is editable in named `HomePage` fields, grouped into
  admin panels.
- The three service cards are an orderable child model and editable inline.
- The hero image is a Wagtail image field with a dark gradient fallback when no
  image is uploaded.
- The contact form saves `ContactSubmission` records and sends an email when
  `CONTACT_EMAIL` is configured. Development uses the console email backend.
- Contact submissions have a Wagtail admin viewset at
  `/admin/contactsubmission/`.
- The approved demo CSS was ported into the Tailwind entry point.
- `0004_seed_homepage` seeds the approved copy and service cards.
- `.dockerignore` now excludes `.pgdata/` and `db/dumps/` so Docker builds do
  not fail on the root-owned database directory.
- The Wagtail admin login mark, sidebar branding, and favicon now use the goat
  instead of the Wagtail bird. The admin sidebar logo is sized with
  `wagtailadmin/css/goat-branding.css`.
- The page explorer title was showing the old "Welcome to your new Wagtail site!"
  draft title because the seed migration updated `title` but not `draft_title`.
  Migration `0006` syncs it, and the admin sidebar now has a direct **Homepage**
  link to the edit form.
- Mobile services spacing was tightened (no double rule above the first card) and
  the manifesto goat is centered on small screens.
- Shared palette, type, layout, and motion values now live in
  `backend/static-src/css/tokens.css` (Tailwind v4 `@theme static`), with
  component CSS using those tokens. The design-token convention is routed from
  `instructions/project_conventions/design_and_tokens.md`.

Checks run:

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py test       # 10 tests passed
docker compose exec tailwind npm run build:css
```

Visual checks: 1440px desktop and 500px mobile captures of the running page.

Follow-ups:

- Create the first admin user:
  `docker compose exec web python manage.py createsuperuser`
- Set `CONTACT_EMAIL` in `.env`; for real delivery, set
  `DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` and the
  `EMAIL_*` SMTP values.
- Upload the final hero image in the Wagtail admin.
- Replace the placeholder GrannyCoded testimonial and point
  `portfolio_url` at the real portfolio page once it exists.
- Replace the placeholder phone link when the VOIP number is live.
