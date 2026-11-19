"""Template helpers for the public site."""

from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter
def absolute_url(value, request):
    """Return an absolute URL for local and remote storage values."""
    if not value:
        return ""

    if urlparse(str(value)).scheme in {"http", "https"}:
        return value

    return request.build_absolute_uri(value)
