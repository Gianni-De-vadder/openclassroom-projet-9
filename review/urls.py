from django.urls import path
from .views import create_ticket, tickets

urlpatterns = [
    # ...
    path("create_ticket/", create_ticket, name="create_ticket"),
    path("posts/", tickets, name="tickets"),
]
