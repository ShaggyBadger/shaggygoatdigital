# How-it-works SEO and inquiry measurement

## Goal and scope

Help local small-business owners understand the website build process, see
examples, and start an inquiry. Give the process page a distinct search title and
measure organic discovery and assisted inquiries after launch. Use the existing
[launch plan](site-launch.md) for offer approvals and production cutover.

## Tickets and acceptance

### SEO-1 · Align Wagtail copy and search metadata

- Update the existing Process Page draft in Wagtail. Proposed SEO title is
  “Small Business Website Design Process | Shaggy Goat Digital,” H1 is
  “How we build your website,” and search description is “See how we build small
  business websites, from a free homepage preview and fixed quote to launch,
  full ownership, and $50/month maintenance.”
- Introduce the free first-screen preview in the opening. Replace the inaccurate
  client-effort summary with what owners actually do across the five steps.
- Acceptance — Preview shows the approved offer, one descriptive H1, and five
  steps consistent with the opening. After publication, rendered HTML at
  `/how-it-works/` has the approved title and description, with neither old
  “four steps” nor “from an email” language in the search or social metadata.
- Dependencies — Confirm copy and offer against the launch plan before
  publication. SEO-2 can proceed alongside this ticket.
- Touchpoints — Wagtail Process Page content and Promote fields.
  `backend/templates/base.html` renders the search and social metadata.

### SEO-2 · Add a path to examples

- Add “Sites we've built” as a secondary link beside the closing inquiry CTA.
- Acceptance — On mobile and desktop the inquiry CTA is clearly primary and
  reaches the homepage contact section. The secondary link reaches the published
  portfolio, which returns HTTP 200 and shows approved work before launch.
- Dependencies — Portfolio content approval for launch.
- Touchpoints — `backend/pages/templates/pages/process_page.html`,
  `backend/static-src/css/process.css`, and `backend/pages/tests.py` if a
  regression check is needed.

### SEO-3 · Verify crawl signals on the public origin

- Check the Wagtail Site hostname and public HTTPS handling. Locally the sitemap
  omits port 8000 while the canonical and robots sitemap reference include it.
- Acceptance — The public page returns HTTP 200 and its canonical matches the
  absolute HTTPS entry in the sitemap. The public robots file allows the page
  and points to the working public sitemap. Check for unintended noindex in HTML
  and response headers. Capture Search Console URL Inspection status and submit
  the sitemap once property access is available.
- Dependencies — Finish SEO-1 and SEO-2 before approving the release. Verify on
  the confirmed production origin during launch cutover.
- Touchpoints — Wagtail Site settings, `backend/config/urls.py`,
  `backend/templates/base.html`, and `backend/templates/robots.txt`.

### SEO-4 · Measure discovery and assisted inquiries

- Use Search Console for organic impressions and clicks filtered to the exact
  public process URL. Record a first 28-day baseline once data is available.
- Acceptance — In the approved analytics setup, report successful contact form
  submissions from sessions that viewed the process page before submitting.
  Verify one event for an accepted submission and zero for an invalid submission,
  a CTA click, or a refresh. Keep inquiry fields and contact details out of
  analytics payloads. Document where both reports live and their date range.
- Dependencies — Confirm analytics provider, consent behavior, and access before
  instrumentation. The submission check can run locally while launch is pending.
  Public reporting depends on SEO-3 and data availability.
- Touchpoints — Existing analytics integration if available,
  `backend/home/models.py` contact success path, and `backend/templates/base.html`.

## Implementation status

- SEO-1 — Wagtail revision 42 is ready for local review. Preview verified the
  title, one H1, five steps, and matching search and social descriptions.
  Publish after copy and offer approval, then verify the live HTML.
- SEO-2 — Implemented and verified in Chrome at 320px and 1440px. The local
  portfolio returns HTTP 200 and shows GrannyCoded. Launch asset approval is
  pending.
- SEO-3 — Changed the local Wagtail Site port to 8000 and restarted the web
  service to refresh its cache. The live local response, sitemap, canonical,
  and robots file now agree. Public and Search Console checks remain at cutover.
- SEO-4 — Google Analytics is intended for client websites. Tracking inquiries
  on Shaggy Goat Digital itself remains a separate, deferred decision.
