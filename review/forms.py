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


from django import forms
from .models import Ticket, Review


from django import forms
from .models import Ticket, Review


class TicketReviewForm(forms.Form):
    title = forms.CharField(
        label="Titre du ticket", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Description du ticket",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = forms.ChoiceField(
        label="Note de la critique",
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    headline = forms.CharField(
        label="Titre de la critique",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    body = forms.CharField(
        label="Corps de la critique",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    def save(self, user):
        ticket = Ticket.objects.create(
            title=self.cleaned_data["title"],
            description=self.cleaned_data["description"],
            user=user,
        )
        review = Review.objects.create(
            ticket=ticket,
            user=user,
            headline=self.cleaned_data["headline"],
            body=self.cleaned_data["body"],
            rating=self.cleaned_data["rating"],
        )
        return ticket, review
