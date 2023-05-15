from django.urls import path
from .views import (
    create_ticket,
    tickets,
    subscription_view,
    unsubscribe,
    delete_ticket,
    create_review,
    review_detail_view,
    search_users,
    delete_review,
    ticket_detail,
)

urlpatterns = [
    # ...
    path("create_ticket/", create_ticket, name="create_ticket"),
    path("posts/", tickets, name="tickets"),
    path("posts/<int:ticket_id>/delete/", delete_ticket, name="delete_ticket"),
    path("abonnement/", subscription_view, name="subscription"),
    path("search_users/", search_users, name="search_users"),
    path("unsubscribe/<int:user_id>/", unsubscribe, name="unsubscribe"),
    path("create_review/<int:ticket_id>/", create_review, name="create_review"),
    path("delete_review/<int:review_id>/", delete_review, name="delete_review"),
    path("<int:review_id>/", review_detail_view, name="review_detail"),
    path("review/tickets/<int:ticket_id>/", ticket_detail, name="ticket_detail"),
]
