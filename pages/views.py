from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from review.models import UserFollows, Ticket, Review
from django.db.models import Q, Value, CharField
from itertools import chain


from django.db.models import Q

@login_required
def home_view(request):
    following_users = UserFollows.objects.filter(user=request.user).values("followed_user")
    user = request.user

    # Modifier la requête des tickets pour inclure également les tickets de l'utilisateur
    tickets = Ticket.objects.filter(
        Q(user__in=following_users) | Q(user=user)
    ).order_by("-time_created")

    reviews = Review.objects.filter(
        Q(user__in=following_users) | Q(ticket__user=user)
    )

    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    tickets.annotate(content_type=Value('TICKET', CharField()))

    context = {
        "tickets": tickets,
        "reviews": reviews,
    }
    return render(request, "pages/home.html", context)
