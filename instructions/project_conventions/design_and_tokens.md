# Design and tokens

The canonical design values live in
[`backend/static-src/css/tokens.css`](../../backend/static-src/css/tokens.css).

It defines the palette, font stacks, layout widths/gutters, navigation heights,
and motion timings through Tailwind v4's `@theme static`. Component CSS uses
`var(--color-gold)` and friends; templates can use the generated utilities
(`text-gold`, `bg-stone`, `border-line`, `font-display`, etc.).

- Change a shared value in `tokens.css`, not in a component stylesheet.
- Keep component-specific decisions (hero masking, type scales, spacing for one
  section) with the component. Promote a value to a token only when it is
  reused or changes the brand.
- Rebuild after changing tokens:
  `docker compose exec tailwind npm run build:css`. The watcher normally
  rebuilds; `site.css` is generated and ignored.
- Never add a new hardcoded hex value to component CSS. Add a semantic token
  instead.

Static assets bake their colors in: `backend/static/brand/shaggy-goat-icon.svg`
(gold), the favicon/PNG app icons, and the `theme-color` meta in
`backend/templates/base.html`. Regenerate or update those separately when the
palette changes.

The Wagtail admin chrome uses Wagtail's own theme. Only the goat mark and its
sizing are customized in `backend/static/wagtailadmin/css/goat-branding.css`.
