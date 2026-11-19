# Landing page restructure

## Goal

Keep the landing page focused on one job: get the visitor to the contact form.
Move proof and personality to their own pages.

## Result

Landing page: hero, pain points, what we do, pricing, testimonial, contact. Each
band ends with a link to `#contact`.

- **Sites we've built** (`/sites-weve-built/`) holds the case studies that used
  to sit on the homepage. `PortfolioPage` + `PortfolioItem` in `pages/models.py`,
  seeded by `seed_portfolio_page`. The testimonial block links here.
- **About** (`/about/`) holds the story, vision, mission, the goat explanation,
  and the two-person team. `AboutPage` + `TeamMember`, seeded by `seed_about_page`.
- Nav: How it works, Sites we've built, Testimonials, About, plus one "Start a
  project" button. Pricing, Work, Why the goat, and the duplicate Contact link
  are gone.
- Section backgrounds alternate: black hero, stone pain, black services, stone
  pricing, black testimonials, bone contact.
- The climbing-goat illustration was removed at the owner's request.

## Copy

- Pain intro stops at "Anyone can. Wix, Squarespace, and a weekend will get you a
  site." The close is now "A goat can climb a wall. You still wouldn't hire it to
  build the house."
- Pricing tiers renamed for buyers, not for the studio: Starter site, Sell or
  book, Custom build. Page counts removed. Self-editing framed as "A site you can
  update yourself".
- "Brochure" is gone from public copy; it stays as an internal contact-form value.

## Shared code

`ClosingCtaMixin` plus `closing_cta_panel()` in `pages/models.py` hold the
closing call to action used by How it works, Sites we've built, and About.

## Verification

21 tests pass, `makemigrations --check` clean, `/`, `/how-it-works/`,
`/sites-weve-built/`, `/about/`, `/privacy/` and `/sitemap.xml` return 200,
rendered at 1440px and 390px.

## Follow-up

Add photos to the About team cards, upload the GrannyCoded screenshot on
production (it lives in the dev media bucket), and decide whether to keep the
pricing band on the landing page or move it.

## Follow-up pass (same day)

- `SiteSettings` (`home/models.py`, Wagtail site settings) now owns the nav
  button label/URL and the footer tagline, so they are edited once under
  Settings -> Site settings and apply to every page. The duplicate fields came
  off `HomePage`.
- Team cards on About render a 4:5 portrait frame with a placeholder mark when
  no photo is set; `TeamMember.photo` carries help text about the crop.
- Admin check: HomePage and its four children (`how-it-works`, `privacy`,
  `sites-weve-built`, `about`) are live and editable under Pages in the Wagtail
  admin.
