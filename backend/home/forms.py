from django import forms

from .models import CONTACT_NEED_CHOICES


class ContactForm(forms.Form):
    """The homepage inquiry form."""

    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={"placeholder": "Your name", "autocomplete": "name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "you@example.com", "autocomplete": "email"}
        ),
    )
    business = forms.CharField(
        max_length=160,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "What do you do?", "autocomplete": "organization"}
        ),
    )
    need = forms.ChoiceField(
        choices=CONTACT_NEED_CHOICES,
        label="What do you need?",
    )
    message = forms.CharField(
        required=False,
        label="What are you running?",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "A sentence or two is plenty.",
            }
        ),
    )
