# Phone contact on homepage inquiries

Allow an email address, a phone number, or both. Update the form and
homepage template, then store and surface the phone number in Wagtail
and inquiry notifications. Verify phone-only, email-only, and missing
contact details through the homepage and apply the schema change locally.

Completed in the home app's form, template, submission model, Wagtail
viewset, and notification service. Applied migration 0020 in local
Compose. All 15 homepage tests passed and the local page rendered the
phone field and contact instructions.
