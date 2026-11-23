# Sites we’ve built portfolio polish

## Goal and scope

Make `/sites-weve-built/` a credible proof page for prospective clients. Bring
the GrannyCoded case study into view sooner, explain what the build changed,
and give readers a clear path to the live storefront and inquiry form. Start
with the one published project. Use the [launch plan](site-launch.md) for
content approval and publication.

## Tickets and acceptance

### PORT-1 · Sharpen the case study and search preview

- Edit the latest local Wagtail revision. Keep “Sites we’ve built” as the H1.
  Proposed intro — “See how we built a storefront for GrannyCoded, a clothing
  maker selling one-of-a-kind pieces and taking custom orders.”
- Keep the problem, build, and outcome structure. The outcome describes how
  GrannyCoded launched her own shop after selling on Etsy and saw more local
  interest when sharing it through business cards.
- Proposed SEO title — “Small Business Website Portfolio | Shaggy Goat Digital”.
  Proposed description — “See how Shaggy Goat Digital built a custom online
  shop for GrannyCoded, with checkout for one-of-a-kind clothing and a form
  for custom orders.”
- Acceptance — Local preview shows one H1, names the project in the opening,
  and describes the outcome without an unverified sales claim. The approved
  title and description render in search and social metadata. Verify the same
  public HTML after publication.
- Dependencies — Independent of PORT-2 and PORT-3. Review copy before publishing.
- Touchpoints — Wagtail Portfolio Page and item fields, Promote tab, and
  `backend/templates/base.html` for metadata rendering.

### PORT-2 · Improve the case study hierarchy

- Reduce the gap before the first project, especially on mobile. Make the
  project H2 distinct from the body copy and give it space before the facts.
- Acceptance — At 390px and 1440px, the first project appears closer to the
  intro, its headline is visually distinct, and the article has no horizontal
  overflow. Verify visible keyboard focus and working links to GrannyCoded and
  the homepage inquiry form. Verify a project without a screenshot still reads
  cleanly.
- Dependencies — Can proceed alongside PORT-1. Agree on rendered card widths
  before setting PORT-3's image sizing.
- Touchpoints — `backend/static-src/css/input.css`, shared design tokens, and
  `backend/pages/templates/pages/portfolio_page.html` if markup needs adjustment.

### PORT-3 · Serve a lighter screenshot on mobile

- Use responsive Wagtail renditions of the existing GrannyCoded screenshot.
  Match the browser's image sizing hint to the portfolio card widths.
- Acceptance — Inspect the browser's selected image and transfer size at 390px
  at 1× and on desktop. The mobile image transfers less than the current
  approximately 530 KB PNG. The desktop image remains sharp at its displayed
  width. The image has accurate alt text and intrinsic dimensions, and missing
  screenshots still render a text-only card.
- Dependencies — Verify against PORT-2's final layout. Use the existing
  screenshot and verify rendition URLs against the configured media storage.
- Touchpoints — `backend/pages/templates/pages/portfolio_page.html` and
  `backend/pages/tests.py` if a regression check is needed.

## Integration check

Preview the Wagtail copy with the combined layout and image changes. Rebuild
CSS through Compose, run the page tests, and check both viewport sizes before
publishing. After approved publication, confirm the live HTML and destinations.

## Implementation status

- PORT-1 — Wagtail draft 52 contains the revised outcome and passed preview checks. Review and publish
  the copy, then verify the live HTML.
- PORT-2 — Chrome at 390px and 1440px verified the measured spacing, larger
  headline, keyboard focus, and absence of horizontal overflow. The combined
  preview also rendered correctly with the project image omitted.
- PORT-3 — At 1× Chrome selected the 400px WebP at 390px and the 600px WebP
  at 1440px. The files are 15,012 and 27,072 bytes respectively. Both media
  URLs returned HTTP 200. The prior PNG was 530,066 bytes.
- Verification — Compose CSS build, nine page tests, and `git diff --check` passed.
