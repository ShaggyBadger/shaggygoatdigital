"""Create the privacy policy page below the homepage.

Idempotent: re-running only fills a page whose body is empty, so admin edits
survive.
"""

from django.core.management.base import BaseCommand, CommandError

from home.models import HomePage
from pages.models import ContentPage

BODY = """
<p>Last updated: 22 November 2026.</p>

<h2>Who this covers</h2>
<p>This is the website of Shaggy Goat Digital, LLC, a web design and development
business in North Carolina. This page explains what happens to anything you send
us through it.</p>

<h2>What we collect</h2>
<p>What you type into the contact form:</p>
<ul>
  <li>Your name</li>
  <li>Your email address, phone number, or both</li>
  <li>Your business name, if you give it</li>
  <li>The kind of work you are asking about</li>
  <li>Whatever you write in the message field</li>
</ul>
<p>We also record when the form was submitted, and our server and hosting
provider keep standard log lines such as IP address, requested URL, and browser,
for security and troubleshooting.</p>

<h2>Why we have it</h2>
<p>To reply to you and to quote the work. That is the whole purpose. We do not
sell it, rent it, or add you to a mailing list you did not ask for.</p>

<h2>Where it lives</h2>
<p>Submissions are stored in a database on our own server, and a copy of each
notification goes to us through our email provider. We keep a submission while
the conversation is live, and after that only as long as we need the record for
tax and project history. Ask us to delete it and we will.</p>

<h2>Cookies</h2>
<p>The site sets only the cookies needed to make forms work safely: a session
cookie and a CSRF token. There are no advertising cookies and no third-party
tracking scripts. If that ever changes, this page changes first.</p>

<h2>Who else sees it</h2>
<p>Our hosting and email providers, as part of running the site. They process
the data on our behalf and do not use it for anything else. We do not share it
with anyone else unless the law requires it.</p>

<h2>Your choices</h2>
<p>Write to us and we will show you what we hold, correct it, or delete it. You
can also ask us to stop contacting you, and we will stop.</p>

<h2>Security</h2>
<p>The site runs over HTTPS, and access to the admin and the database is limited
to us. No system is perfect. If a breach ever affects information you gave us, we
will tell you.</p>

<h2>Children</h2>
<p>This site is for businesses. We do not knowingly collect information from
anyone under 13.</p>

<h2>Changes</h2>
<p>If this policy changes, the date at the top changes with it.</p>

<h2>Contact</h2>
<p>Questions about any of this go through the
<a href="/#contact">contact form</a>. We answer those the same way we answer
everything else.</p>
"""

INTRO = "What this site collects, why we have it, and how to get rid of it."


class Command(BaseCommand):
    help = "Create the privacy policy page below the homepage."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            raise CommandError("No homepage exists to attach the page to.")

        page = ContentPage.objects.child_of(home).filter(slug="privacy").first()
        created = page is None

        if created:
            page = ContentPage(
                title="Privacy Policy",
                slug="privacy",
                seo_title="Privacy policy | Shaggy Goat Digital, LLC",
                search_description=(
                    "What this site collects, why, where it is stored, and how "
                    "to have it deleted."
                ),
            )
            home.add_child(instance=page)

        page.eyebrow = "The boring part"
        page.intro = INTRO
        if not page.body:
            page.body = BODY

        page.save_revision().publish()
        action = "Created" if created else "Refreshed"
        self.stdout.write(self.style.SUCCESS(f"{action} {page.url}"))
