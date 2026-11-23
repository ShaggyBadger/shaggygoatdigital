from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.models import Site

from .models import ContactSubmission


class ContactSubmissionViewSet(ModelViewSet):
    model = ContactSubmission
    menu_label = "Contact submissions"
    menu_icon = "mail"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ("name", "email", "phone", "business", "need", "created_at")
    list_filter = ("need",)
    search_fields = ("name", "email", "phone", "business", "message")
    inspect_view_enabled = True
    form_fields = ("name", "email", "phone", "business", "need", "message")


@hooks.register("register_admin_viewset")
def register_contact_submission_viewset():
    return ContactSubmissionViewSet()


@hooks.register("insert_global_admin_css")
def goat_admin_branding_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtailadmin/css/goat-branding.css"),
    )


@hooks.register("register_admin_menu_item")
def register_homepage_menu_item():
    """Put the homepage edit form one click away from the admin sidebar."""
    site = Site.objects.filter(is_default_site=True).first()
    if site is None:
        return None

    return MenuItem(
        "Homepage",
        reverse("wagtailadmin_pages:edit", args=[site.root_page_id]),
        name="homepage-edit",
        icon_name="home",
        order=90,
    )
