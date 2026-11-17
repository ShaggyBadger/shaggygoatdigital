from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

from .services import notify_contact_submission

CONTACT_NEED_CHOICES = [
    ("brochure", "A brochure site"),
    ("shop", "A shop or booking"),
    ("not-sure", "Not sure yet"),
]


class HomePage(Page):
    """The Shaggy Goat Digital homepage."""

    max_count = 1

    hero_heading = models.CharField(
        max_length=160,
        default="Websites with a backbone.",
    )
    hero_intro = models.TextField(
        default=(
            "We build sharp, fast sites for local businesses that plan to be around "
            "a while. We're sure-footed on the technical parts, stubborn about the "
            "details, and still here after launch."
        ),
    )
    hero_cta_label = models.CharField(
        max_length=80,
        default="Tell us what you're building",
    )
    hero_cta_url = models.CharField(max_length=200, default="#contact")
    hero_secondary_label = models.CharField(max_length=80, default="Call or text")
    hero_secondary_url = models.CharField(max_length=200, default="#contact")
    hero_price_line = RichTextField(
        features=["bold"],
        default=(
            "<p>Brochure sites from <strong>$500</strong>. Maintenance "
            "<strong>$50 a month</strong>. Custom work quoted after we talk.</p>"
        ),
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_image_credit = models.CharField(
        max_length=160,
        default="Josh Ballard. The goat in question.",
    )

    services_heading = models.CharField(max_length=80, default="What we do")
    services_intro = models.CharField(
        max_length=200,
        default="Pick the sentence that sounds like your week. We'll do the part that isn't fun.",
    )
    services_footnote = models.TextField(
        default=(
            "If two of those sound like your week, start with a brochure site. "
            "We'll tell you when you need the rest."
        ),
    )

    pricing_kicker = models.CharField(
        max_length=80,
        default="Brochure sites from",
    )
    pricing_amount = models.CharField(max_length=40, default="$500")
    pricing_body = models.TextField(
        default=(
            "Brochure sites start at $500. Maintenance is $50 a month. Shops, "
            "booking, and custom work get a written quote before we build."
        ),
    )
    pricing_note = models.CharField(
        max_length=160,
        default="We put it in writing first. We're stubborn that way.",
    )

    portfolio_heading = models.CharField(max_length=80, default="Portfolio")
    portfolio_intro = models.CharField(
        max_length=200,
        default="A custom storefront, a catalog, and a client who can run it without us.",
    )
    portfolio_project_label = models.CharField(
        max_length=120,
        default="GrannyCoded / Custom storefront",
    )
    portfolio_project_summary = models.TextField(
        default=(
            "Catalog, checkout, and a content system the owner can update herself. "
            "She adds a piece, it appears. That's the whole point."
        ),
    )
    portfolio_quote = models.TextField(
        default="I can add a piece without calling anyone.",
    )
    portfolio_quote_author = models.CharField(max_length=80, default="Hannah")
    portfolio_quote_company = models.CharField(max_length=80, default="GrannyCoded")
    portfolio_quote_url = models.URLField(default="https://grannycoded.com")
    portfolio_cta_label = models.CharField(
        max_length=80,
        default="See the portfolio",
    )
    portfolio_url = models.CharField(
        max_length=200, default="https://grannycoded.com"
    )

    manifesto_heading = models.CharField(max_length=80, default="Why the goat?")
    manifesto_body = RichTextField(
        features=["bold", "italic", "link"],
        default=(
            "<p>Goats climb what they shouldn't and stand where they shouldn't. "
            "They also refuse to fall off. We build websites with the same "
            "temperament: sure-footed, stubborn, and hard to knock down.</p>"
            "<p>The work is the work. We show up, build it, and answer the phone.</p>"
        ),
    )
    manifesto_tagline = models.CharField(
        max_length=160,
        default="The goat is the mascot. The backbone is the product.",
    )

    contact_heading = models.CharField(
        max_length=120,
        default="Tell us what you're running.",
    )
    contact_intro = models.TextField(
        default=(
            "A short note is enough. We'll reply with questions, a rough price, "
            "and a straight answer. If we're not the right fit, we'll say so."
        ),
    )
    contact_phone_label = models.CharField(max_length=80, default="Call or text")
    contact_phone_url = models.CharField(max_length=200, default="#contact")
    contact_submit_label = models.CharField(max_length=80, default="Send it")
    contact_note = models.CharField(max_length=80, default="No scapegoats.")

    nav_cta_label = models.CharField(max_length=80, default="Start a project")
    nav_cta_url = models.CharField(max_length=200, default="/#contact")
    footer_tagline = models.CharField(
        max_length=160,
        default="Websites with a backbone. And a goat.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_heading"),
                FieldPanel("hero_intro"),
                FieldPanel("hero_cta_label"),
                FieldPanel("hero_cta_url"),
                FieldPanel("hero_secondary_label"),
                FieldPanel("hero_secondary_url"),
                FieldPanel("hero_price_line"),
                FieldPanel("hero_image"),
                FieldPanel("hero_image_credit"),
            ],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("services_heading"),
                FieldPanel("services_intro"),
                InlinePanel("service_cards", label="Service cards", min_num=1, max_num=6),
                FieldPanel("services_footnote"),
            ],
            heading="Services",
        ),
        MultiFieldPanel(
            [
                FieldPanel("pricing_kicker"),
                FieldPanel("pricing_amount"),
                FieldPanel("pricing_body"),
                FieldPanel("pricing_note"),
            ],
            heading="Pricing",
        ),
        MultiFieldPanel(
            [
                FieldPanel("portfolio_heading"),
                FieldPanel("portfolio_intro"),
                FieldPanel("portfolio_project_label"),
                FieldPanel("portfolio_project_summary"),
                FieldPanel("portfolio_quote"),
                FieldPanel("portfolio_quote_author"),
                FieldPanel("portfolio_quote_company"),
                FieldPanel("portfolio_quote_url"),
                FieldPanel("portfolio_cta_label"),
                FieldPanel("portfolio_url"),
            ],
            heading="Portfolio",
        ),
        MultiFieldPanel(
            [
                FieldPanel("manifesto_heading"),
                FieldPanel("manifesto_body"),
                FieldPanel("manifesto_tagline"),
            ],
            heading="Why the goat",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_heading"),
                FieldPanel("contact_intro"),
                FieldPanel("contact_phone_label"),
                FieldPanel("contact_phone_url"),
                FieldPanel("contact_submit_label"),
                FieldPanel("contact_note"),
            ],
            heading="Contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("nav_cta_label"),
                FieldPanel("nav_cta_url"),
                FieldPanel("footer_tagline"),
            ],
            heading="Navigation and footer",
        ),
    ]

    class Meta:
        verbose_name = "home page"

    def serve(self, request, *args, **kwargs):
        """Render the page and accept contact-form submissions."""
        from .forms import ContactForm

        if request.method == "POST":
            if request.POST.get("website"):
                return redirect(f"{self.url}#contact")

            form = ContactForm(request.POST)
            if form.is_valid():
                submission = ContactSubmission.objects.create(**form.cleaned_data)
                notify_contact_submission(submission)
                messages.success(
                    request,
                    "Got it. We'll get back to you shortly.",
                )
                return redirect(f"{self.url}#contact")
            messages.error(request, "Check the form and try again.")
        else:
            form = ContactForm()

        return render(
            request,
            "home/home_page.html",
            {"page": self, "form": form},
        )


class ServiceCard(Orderable):
    """One card in the homepage services grid."""

    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="service_cards",
    )
    title = models.CharField(max_length=80)
    description = models.TextField()
    price_label = models.CharField(max_length=80)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("price_label"),
    ]

    def __str__(self) -> str:
        return self.title


class ContactSubmission(models.Model):
    """A contact-form submission kept in the Wagtail admin."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    business = models.CharField(max_length=160, blank=True)
    need = models.CharField(max_length=20, choices=CONTACT_NEED_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contact submission"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
