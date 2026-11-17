"""Focused services for the homepage app."""

import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_contact_submission(submission) -> None:
    """Email a new submission when a destination address is configured."""
    if not settings.CONTACT_EMAIL:
        return

    body = "\n".join(
        [
            f"Name: {submission.name}",
            f"Email: {submission.email}",
            f"Business: {submission.business or 'Not provided'}",
            f"Needs: {submission.get_need_display()}",
            "",
            "Message:",
            submission.message or "Not provided",
        ]
    )

    try:
        send_mail(
            subject=f"New website inquiry from {submission.name}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Could not send contact notification for submission %s",
            submission.pk,
        )
