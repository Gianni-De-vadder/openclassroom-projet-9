from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]

    def __init__(self, *args, **kwargs):
        ticket_title = kwargs.pop("ticket_title", None)
        super().__init__(*args, **kwargs)
        if ticket_title:
            self.fields["headline"].initial = ticket_title
