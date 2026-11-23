import re

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
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "aria-describedby": "contact-method-hint",
            }
        ),
    )
    phone = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "autocomplete": "tel",
                "aria-describedby": "contact-method-hint",
            }
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

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            return phone

        # Accept grouped digits and common separators, keeping the submitted
        # formatting for the inquiry and its notification.
        digit_or_group = r"(?:[0-9]|\([0-9]+\))"
        if not re.fullmatch(rf"\+?{digit_or_group}(?:[ .-]*{digit_or_group})*", phone):
            raise forms.ValidationError("Enter a valid phone number.")

        digits = re.sub(r"[^0-9]", "", phone)
        if phone.startswith("+"):
            valid = 7 <= len(digits) <= 15 and not digits.startswith("0")
        elif digits.startswith(("00", "011")):
            prefix_length = 2 if digits.startswith("00") else 3
            national = digits[prefix_length:]
            valid = 7 <= len(national) <= 15 and not national.startswith("0")
        else:
            valid = len(digits) == 10 or (len(digits) == 11 and digits.startswith("1"))

        if not valid:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        if not self.has_error("email") and not self.has_error("phone"):
            if not (cleaned_data.get("email") or cleaned_data.get("phone")):
                raise forms.ValidationError("Enter an email address or phone number.")
        return cleaned_data
