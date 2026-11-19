from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

from .services import notify_contact_submission

CONTACT_NEED_CHOICES = [
    ("brochure", "A starter site"),
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
            "<p>Starter sites from <strong>$500</strong>. Maintenance "
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

    pain_heading = models.CharField(
        max_length=80,
        default="You could build this yourself.",
    )
    pain_intro = models.TextField(
        default=(
            "Anyone can. Wix, Squarespace, and a weekend will get you a site."
        ),
    )
    pain_footnote = models.CharField(
        max_length=240,
        default=(
            "A goat can climb a wall. You still wouldn't hire it to build the "
            "house."
        ),
    )

    services_heading = models.CharField(max_length=80, default="What we do")
    services_intro = models.CharField(
        max_length=200,
        default="Pick the sentence that sounds like your week. We'll do the part that isn't fun.",
    )
    services_footnote = models.TextField(
        default=(
            "If two of those sound like your week, start small and grow into "
            "the rest. We'll tell you when you actually need it."
        ),
    )

    pricing_heading = models.CharField(max_length=80, default="What it costs")
    pricing_intro = models.TextField(
        default=(
            "Fixed prices, published before we talk. Every project starts with two "
            "documents: an agreement covering who does what and who owns what, and "
            "a statement of work covering scope, price, and dates. The number in "
            "the statement of work is the number on the invoice."
        ),
    )
    pricing_note = models.CharField(
        max_length=160,
        default=(
            "Maintenance is $50 a month: updates, backups, and small changes. "
            "Cancel whenever."
        ),
    )

    testimonials_heading = models.CharField(max_length=80, default="Testimonials")
    testimonials_intro = models.CharField(
        max_length=200,
        default="What it's like to work with us.",
    )
    testimonial_client_label = models.CharField(
        max_length=120,
        default="GrannyCoded / Custom storefront",
    )
    testimonial_quote = models.TextField(
        default=(
            "I sent over product photos and a rough idea of what I wanted. "
            "What came back looked like the business I'd been trying to explain "
            "for years. I can add a piece now without calling anyone."
        ),
    )
    testimonial_author = models.CharField(max_length=80, default="Hannah")
    testimonial_company = models.CharField(max_length=80, default="GrannyCoded")
    testimonial_company_url = models.URLField(default="https://grannycoded.com")

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
                FieldPanel("pain_heading"),
                FieldPanel("pain_intro"),
                InlinePanel("pain_points", label="Hassle", min_num=1, max_num=5),
                FieldPanel("pain_footnote"),
            ],
            heading="Pain points",
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
                FieldPanel("pricing_heading"),
                FieldPanel("pricing_intro"),
                InlinePanel("price_tiers", label="Tier", min_num=1, max_num=3),
                FieldPanel("pricing_note"),
            ],
            heading="Pricing",
        ),
        MultiFieldPanel(
            [
                FieldPanel("testimonials_heading"),
                FieldPanel("testimonials_intro"),
                FieldPanel("testimonial_client_label"),
                FieldPanel("testimonial_quote"),
                FieldPanel("testimonial_author"),
                FieldPanel("testimonial_company"),
                FieldPanel("testimonial_company_url"),
            ],
            heading="Testimonials",
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


class PainPoint(Orderable):
    """One DIY hassle in the pain-points list."""

    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="pain_points",
    )
    title = models.CharField(max_length=60)
    body = models.TextField()

    panels = [
        FieldPanel("title"),
        FieldPanel("body"),
    ]

    def __str__(self) -> str:
        return self.title


class PriceTier(Orderable):
    """One published price tier."""

    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="price_tiers",
    )
    name = models.CharField(max_length=60)
    price = models.CharField(max_length=40)
    blurb = models.TextField()
    features = models.TextField(help_text="One item per line.")

    panels = [
        FieldPanel("name"),
        FieldPanel("price"),
        FieldPanel("blurb"),
        FieldPanel("features"),
    ]

    def __str__(self) -> str:
        return f"{self.name} — {self.price}"


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
