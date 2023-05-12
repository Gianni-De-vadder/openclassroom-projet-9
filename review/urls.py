from django.urls import path
from .views import create_ticket, tickets, subscription_view, unsubscribe

urlpatterns = [
    # ...
    path("create_ticket/", create_ticket, name="create_ticket"),
    path("posts/", tickets, name="tickets"),
    path("abonnement/", subscription_view, name="subscription"),
    path("unsubscribe/<int:user_id>/", unsubscribe, name="unsubscribe"),
]
