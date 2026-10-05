from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ["check_in", "check_out", "guests"]

        widgets = {
            "check_in": forms.DateInput(
                attrs={"type": "date"}
            ),
            "check_out": forms.DateInput(
                attrs={"type": "date"}
            ),
            "guests": forms.NumberInput(
                attrs={"min": 1}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError(
                    "Check-out date must be after check-in date."
                )

        return cleaned_data