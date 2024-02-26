from django import forms
from ..models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["customer", "room", "start_datetime", "end_datetime", "payment_info"]
