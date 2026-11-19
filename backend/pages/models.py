"""Site pages that are not the homepage."""

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class ProcessStep(Orderable):
    """One numbered step in the build."""

    page = ParentalKey(
        "pages.ProcessPage", on_delete=models.CASCADE, related_name="steps"
    )
    title = models.CharField(max_length=120)
    body = models.TextField()
    client_note = models.CharField(
        max_length=200,
        blank=True,
        help_text="What the client does at this step, in one line.",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("body"),
        FieldPanel("client_note"),
    ]


class StackItem(Orderable):
    """One row of the spec sheet."""

    page = ParentalKey(
        "pages.ProcessPage", on_delete=models.CASCADE, related_name="stack_items"
    )
    label = models.CharField(max_length=60)
    value = models.CharField(max_length=240)

    panels = [
        FieldPanel("label"),
        FieldPanel("value"),
    ]


class FaqItem(Orderable):
    """One question and its answer."""

    page = ParentalKey(
        "pages.ProcessPage", on_delete=models.CASCADE, related_name="faq_items"
    )
    question = models.CharField(max_length=160)
    answer = models.TextField()

    panels = [
        FieldPanel("question"),
        FieldPanel("answer"),
    ]


class ProcessPage(Page):
    """How the work happens: the steps, the stack, what the client owns."""

    max_count = 1

    eyebrow = models.CharField(max_length=60, default="The process")
    heading = models.CharField(max_length=120, default="How this works.")
    intro = models.TextField(
        default=(
            "Four steps from one sentence in a form to a site you can send people "
            "to. Here is the whole thing, in order, including the parts that "
            "usually get left until after the invoice."
        )
    )

    steps_heading = models.CharField(max_length=80, default="Four steps, start to finish")
    steps_intro = models.CharField(
        max_length=240,
        default=(
            "Most of these take a day or two. You handle the first one and the "
            "third one. We do the rest."
        ),
    )

    stack_heading = models.CharField(max_length=80, default="What's under the hood")
    stack_intro = models.TextField(
        default=(
            "Most small business sites are a page builder, forty plugins, and a "
            "monthly bill that only goes up. This is a different set of decisions."
        )
    )
    stack_quip = models.CharField(
        max_length=160,
        blank=True,
        default="A goat doesn't need a plugin to climb a wall.",
    )

    ownership_heading = models.CharField(max_length=80, default="What you own")
    ownership_body = RichTextField(
        default=(
            "<p>On final payment, the site, the code, the content, and the data "
            "are yours. We hold the domain while the build is running and "
            "transfer it whenever you ask, including at handover.</p>"
            "<p>If you move to another host, the files go with you and we help "
            "with the move. Keeping a client by holding the keys is a strange "
            "way to run a business.</p>"
        ),
        features=["bold", "italic", "link"],
    )

    fit_heading = models.CharField(max_length=80, default="Who this isn't for")
    fit_body = RichTextField(
        default=(
            "<p>If you need twenty pages, a customer portal, or a marketing "
            "team's worth of campaign landing pages, we're the wrong shop and "
            "we'll say so on the first call.</p>"
            "<p>We build small sites well: five pages, one job, quick. That's "
            "the whole product.</p>"
        ),
        features=["bold", "italic", "link"],
    )

    faq_heading = models.CharField(max_length=80, default="Questions that come up")
    faq_intro = models.CharField(
        max_length=200,
        default="If yours isn't here, ask it. We answer the same day.",
    )

    cta_heading = models.CharField(
        max_length=120, default="Tell us what you're running"
    )
    cta_body = models.TextField(
        default=(
            "One sentence is enough. We'll reply with questions, a rough price, "
            "and a straight answer."
        )
    )
    cta_label = models.CharField(max_length=80, default="Start a project")
    cta_url = models.CharField(max_length=200, default="/#contact")
    cta_note = models.CharField(max_length=80, default="No scapegoats.")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("heading"),
                FieldPanel("intro"),
            ],
            heading="Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("steps_heading"),
                FieldPanel("steps_intro"),
                InlinePanel("steps", label="Step"),
            ],
            heading="Steps",
        ),
        MultiFieldPanel(
            [
                FieldPanel("stack_heading"),
                FieldPanel("stack_intro"),
                FieldPanel("stack_quip"),
                InlinePanel("stack_items", label="Spec row"),
            ],
            heading="Under the hood",
        ),
        MultiFieldPanel(
            [
                FieldPanel("ownership_heading"),
                FieldPanel("ownership_body"),
            ],
            heading="Ownership",
        ),
        MultiFieldPanel(
            [
                FieldPanel("fit_heading"),
                FieldPanel("fit_body"),
            ],
            heading="Fit",
        ),
        MultiFieldPanel(
            [
                FieldPanel("faq_heading"),
                FieldPanel("faq_intro"),
                InlinePanel("faq_items", label="Question"),
            ],
            heading="FAQ",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cta_heading"),
                FieldPanel("cta_body"),
                FieldPanel("cta_label"),
                FieldPanel("cta_url"),
                FieldPanel("cta_note"),
            ],
            heading="Closing call to action",
        ),
    ]

    promote_panels = Page.promote_panels

    template = "pages/process_page.html"
