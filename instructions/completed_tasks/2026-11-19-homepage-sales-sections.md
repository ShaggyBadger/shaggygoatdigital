# Homepage sales sections

## Goal

Add the proof and objection-handling sections a buyer needs before contacting
the business, without changing the established visual system. Copy ships as
editable defaults; the owner rewrites it in the Wagtail admin.

## Sections

1. **Pain points** — the DIY hassles (words, photos, phones, getting found),
   placed directly under the hero so visitors recognise themselves before they
   read a service list.
2. **Selected work** — one live case study (GrannyCoded) with problem, what we
   built, outcome, link, optional screenshot and optional quote. Inline list so
   project two is admin work, not a deploy.
3. **What it costs** — three published tiers (Brochure / Shop or booking /
   Custom) replacing the single price band, with the $50 maintenance note kept
   underneath.
4. **Who we are** — Josh and Leah, roles, short bios, optional photos, and
   North Carolina as the location.

## Supporting changes

- Footer and Organization schema mention North Carolina.
- `/how-it-works/` gains the free homepage concept step, before the quote.
- New `ContentPage` type and `/privacy/` page, linked from the footer.

## Files

- `backend/home/models.py`, new migration, `backend/home/migrations/0009_*`
- `backend/home/templates/home/home_page.html` plus `home/sections/*.html`
- `backend/home/templatetags/home_tags.py` (a `lines` filter for tier features)
- `backend/static-src/css/input.css`
- `backend/pages/models.py`, `content_page.html`, `seed_privacy_page.py`,
  `seed_process_page.py`
- `backend/templates/base.html`, `partials/site_footer.html`,
  `partials/site_nav.html`
- `backend/home/tests.py`

## Verification

- `makemigrations --check` reports no changes
- `docker compose exec web python manage.py check`
- `docker compose exec web python manage.py test` passes
- Tailwind build includes the new section classes
- `/`, `/how-it-works/`, `/privacy/` render at 1440px and 400px

## Completion summary (2026-11-19)

**What changed.** Added four homepage sections (pain points, selected work,
three-tier pricing, who we are), the free-homepage-concept step in
`/how-it-works/`, and a `/privacy/` page with a footer link. North Carolina
appears in the team intro, the footer, and the Organization schema.

**Key files.** `backend/home/models.py` and migrations `0009`–`0011`;
`backend/home/templates/home/sections/*.html`; `backend/static-src/css/input.css`;
`backend/pages/models.py` (`ContentPage`) with `content_page.html` and
`seed_privacy_page`; `seed_process_page.py`; `backend/home/tests.py`;
`backend/pages/tests.py`.

**Checks run.** `makemigrations --check` clean, migrations applied, `check`
clean, 16 tests pass, Tailwind build complete, `/`, `/how-it-works/`,
`/privacy/`, `/sitemap.xml` return 200, and pages rendered at 1440px and 390px.

**Follow-up.** Add a GrannyCoded screenshot to the work item, replace the
placeholder bios and prices in the admin, and fill in the real phone number and
contact email.
