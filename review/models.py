from django.conf import settings
from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    image = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("create_review", kwargs={"ticket_id": self.id})

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.headline}"


User = get_user_model()


class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"
