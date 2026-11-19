"""Site pages that are not the homepage."""

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


def closing_cta_panel():
    """The admin panel for the shared closing call to action."""
    return MultiFieldPanel(
        [
            FieldPanel("cta_heading"),
            FieldPanel("cta_body"),
            FieldPanel("cta_label"),
            FieldPanel("cta_url"),
            FieldPanel("cta_note"),
        ],
        heading="Closing call to action",
    )


class ClosingCtaMixin(models.Model):
    """Copy for the closing band shared by the interior pages."""

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

    class Meta:
        abstract = True


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


class ProcessPage(ClosingCtaMixin, Page):
    """How the work happens: the steps, the stack, what the client owns."""

    max_count = 1

    eyebrow = models.CharField(max_length=60, default="The process")
    heading = models.CharField(max_length=120, default="How this works.")
    intro = models.TextField(
        default=(
            "Five steps from one sentence in a form to a site you can send people "
            "to. Here is the whole thing, in order, including the parts that "
            "usually get left until after the invoice."
        )
    )

    steps_heading = models.CharField(max_length=80, default="Five steps, start to finish")
    steps_intro = models.CharField(
        max_length=240,
        default=(
            "Most of these take a day or two. You handle the first one and the "
            "fourth one. We do the rest."
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
        closing_cta_panel(),
    ]

    promote_panels = Page.promote_panels

    template = "pages/process_page.html"


class ContentPage(Page):
    """A plain page for policy and other long-form text."""

    max_count = 5

    eyebrow = models.CharField(max_length=60, blank=True, default="")
    intro = models.TextField(blank=True, default="")
    body = RichTextField(
        blank=True,
        features=["h2", "h3", "bold", "italic", "link", "ol", "ul"],
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("intro"),
                FieldPanel("body"),
            ],
            heading="Content",
        ),
    ]

    template = "pages/content_page.html"


class PortfolioItem(Orderable):
    """One project on the Sites we've built page."""

    page = ParentalKey(
        "pages.PortfolioPage",
        on_delete=models.CASCADE,
        related_name="items",
    )
    client_label = models.CharField(
        max_length=120,
        help_text="Client and build type, such as GrannyCoded / Custom storefront.",
    )
    project_title = models.CharField(max_length=120)
    problem = models.TextField(help_text="What the client was stuck with.")
    built = models.TextField(help_text="What you built, in plain language.")
    outcome = models.TextField(help_text="What changed for the client.")
    url = models.URLField(blank=True, help_text="The live site.")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    quote = models.TextField(blank=True)
    quote_author = models.CharField(max_length=120, blank=True)

    panels = [
        FieldPanel("client_label"),
        FieldPanel("project_title"),
        FieldPanel("problem"),
        FieldPanel("built"),
        FieldPanel("outcome"),
        FieldPanel("url"),
        FieldPanel("image"),
        FieldPanel("quote"),
        FieldPanel("quote_author"),
    ]

    def __str__(self) -> str:
        return f"{self.client_label} — {self.project_title}"


class PortfolioPage(ClosingCtaMixin, Page):
    """The work: one card per project, with the story behind it."""

    max_count = 1

    eyebrow = models.CharField(max_length=60, default="The work")
    intro = models.TextField(
        default=(
            "Live sites, not mockups. Open any of them on your phone and see how "
            "they behave."
        )
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("intro"),
                InlinePanel("items", label="Project", min_num=1, max_num=12),
            ],
            heading="Projects",
        ),
        closing_cta_panel(),
    ]

    template = "pages/portfolio_page.html"


class TeamMember(Orderable):
    """One person on the About page."""

    page = ParentalKey(
        "pages.AboutPage",
        on_delete=models.CASCADE,
        related_name="team_members",
    )
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=80)
    bio = models.TextField()
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("bio"),
        FieldPanel("photo"),
    ]

    def __str__(self) -> str:
        return f"{self.name} — {self.role}"


class AboutPage(ClosingCtaMixin, Page):
    """Who we are, and why the business exists."""

    max_count = 1

    eyebrow = models.CharField(max_length=60, default="About")
    intro = models.TextField(
        default=(
            "Two people in North Carolina, building the websites we kept wishing "
            "our own neighbors had."
        )
    )
    story_heading = models.CharField(max_length=80, default="Why we started")
    story_body = RichTextField(
        default=(
            "<p>We kept running into the same thing. A good electrician, "
            "recommended by three people, with a phone number on a Facebook page "
            "and nothing else. A plumber whose site was built a decade ago and "
            "falls apart on a phone. Someone who does beautiful work and is "
            "invisible unless you already know their name.</p>"
            "<p>So you do the only thing you can: make a list of numbers, call "
            "down it, and reach the company with the ad budget instead. You pay "
            "more, and half the time you get somebody who acts like the call is "
            "an inconvenience.</p>"
            "<p>A business like that doesn't need twenty pages and a content "
            "team. It needs a site that says what it does, where it works, when "
            "it's open, and how to reach a human. Then it needs to keep working "
            "after launch.</p>"
        ),
        features=["bold", "italic", "link", "h2", "h3"],
    )
    mission_heading = models.CharField(max_length=80, default="What we're here for")
    mission_body = RichTextField(
        default=(
            "<p><strong>Vision:</strong> every good local business easy to find, "
            "easy to understand, and easy to call.</p>"
            "<p><strong>Mission:</strong> build small, fast, honest websites for "
            "businesses that plan to be around a while, and stay on the hook "
            "after launch.</p>"
        ),
        features=["bold", "italic", "link"],
    )
    goat_heading = models.CharField(max_length=80, default="Why a goat?")
    goat_body = RichTextField(
        default=(
            "<p>Goats climb what they shouldn't and stand where they shouldn't. "
            "They also refuse to fall off. We build websites with the same "
            "temperament: sure-footed, stubborn, and hard to knock down.</p>"
            "<p>The work is the work. We show up, build it, and answer the phone.</p>"
            "<p><em>The goat is the mascot. The backbone is the product.</em></p>"
        ),
        features=["bold", "italic", "link"],
    )
    team_heading = models.CharField(max_length=80, default="Who we are")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("intro"),
                FieldPanel("story_heading"),
                FieldPanel("story_body"),
                FieldPanel("mission_heading"),
                FieldPanel("mission_body"),
                FieldPanel("goat_heading"),
                FieldPanel("goat_body"),
            ],
            heading="Story",
        ),
        MultiFieldPanel(
            [
                FieldPanel("team_heading"),
                InlinePanel("team_members", label="Person", min_num=1, max_num=6),
            ],
            heading="Who we are",
        ),
        closing_cta_panel(),
    ]

    template = "pages/about_page.html"
