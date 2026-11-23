# Repository review fixes

Make homepage inquiries replyable, disclose the phone data the form collects,
preserve unpublished Wagtail work, and make local database restores atomic.
Use [the launch plan](site-launch.md) for content approval and cutover.

## REV-1 · Validate inquiry phone numbers · P1

Validate phone numbers server-side. Keep both contact fields optional
individually and require at least one. Show a phone field error when a
supplied number is invalid, even if the email is valid.

- **REV-1a** — Valid email-only, phone-only, and combined submissions succeed.
  Accept ordinary US formatting and numbers with an international dialing
  prefix. A valid phone-only inquiry retains the number in Wagtail and in
  the notification.
- **REV-1b** — Blank contact fields still show the existing contact-method
  message. A supplied value such as `not a number` shows a phone field error,
  creates no inquiry, and sends no notification.
- **Verification** — Exercise these cases through the homepage with Django's
  in-memory email backend.
- **Touchpoints** — `backend/home/forms.py`, `backend/home/tests.py`.
  **Dependencies** — None.

## REV-2 · Disclose phone collection in the privacy policy · P2

Update the seed policy and the existing local Wagtail privacy page to list
an email address, a phone number, or both. Keep the description of database
storage and email notifications consistent with the inquiry flow.

- **REV-2a** — A newly seeded privacy page renders the updated disclosure.
- **REV-2b** — The existing Wagtail page has a reviewed draft with the same
  disclosure and an updated date. After approval and publication, verify the
  rendered `/privacy/` before opening public traffic with the phone field.
- **Verification** — Run the privacy page tests, review the existing page in
  Wagtail Preview, then check the published page after approval.
- **Touchpoints** — `backend/pages/management/commands/seed_privacy_page.py`,
  `backend/pages/tests.py`, and the local Wagtail privacy page.
  **Dependencies** — Content approval is required for publication.

## REV-3 · Preserve Wagtail drafts on reseed · P1

Make the portfolio and process seed commands publish on first creation and
leave existing pages untouched by default. Preserve intentional refreshes
through an explicit option. Refuse refresh when the page has unpublished
changes, before making any page or child-row writes.

- **REV-3a** — On a fresh database, both commands create a published page
  with the expected child content. Default reruns keep that content and
  revision count stable.
- **REV-3b** — On a page with a draft title and draft child edits, default
  reruns preserve the live page and the latest revision ID and contents.
  An explicit refresh refuses the same page without writing anything.
- **REV-3c** — For a page with no unpublished changes, an explicit refresh
  still supports the existing missing-content repair, including the process
  page's legacy free-concept step. Repeated refreshes do not duplicate rows.
- **Verification** — Cover fresh creation, draft preservation, and explicit
  refresh for both commands in isolated Django tests.
- **Touchpoints** — The portfolio and process seed commands and
  `backend/pages/tests.py`. **Dependencies** — None. Coordinate test-file
  edits with REV-2.

## REV-4 · Roll back failed local restores · P1

Run the local custom-format restore in one transaction and exit on the first
error. Preserve the existing archive input and local Compose target.

- **REV-4a** — A compatible archive restores successfully into a disposable
  database, and the script reports success.
- **REV-4b** — An archive that fails after restore work has begun makes the
  script exit nonzero without reporting success. Existing schema and sentinel
  data remain intact.
- **Verification** — Run `bash -n` and exercise both cases in a disposable
  Compose checkout with its own database bind mount.
- **Touchpoints** — `scripts/db-restore.sh`. **Dependencies** — None.

## Delivery order

Run REV-1, REV-3, and REV-4 independently. REV-2's Wagtail draft can proceed
alongside them. Serialize edits to `backend/pages/tests.py` for REV-2 and
REV-3. Verify the four tickets before the launch cutover, including the
published privacy page after approval.

## Verification status

- REV-1 — All 17 homepage tests passed in a fresh local Compose test database.
- REV-2 — Local Wagtail revision 60 passed Preview with the updated
  disclosure and date. Approve and publish the draft, then verify
  `/privacy/` before cutover.
- REV-3 — Three focused PostgreSQL regression tests passed for both seed
  commands, including preservation of unpublished child edits.
- REV-4 — A compatible archive restored successfully in disposable Compose.
  A restore that failed on a missing enum exited nonzero, and the original
  tables and sentinel rows survived.
