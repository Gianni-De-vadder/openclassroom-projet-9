from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from review.models import UserFollows, Ticket, Review


@login_required
def home_view(request):
    # Récupérer les utilisateurs auxquels l'utilisateur est abonné
    following_users = UserFollows.objects.filter(user=request.user).values(
        "followed_user"
    )

    # Récupérer les demandes de critique des utilisateurs abonnés
    tickets = Ticket.objects.filter(user__in=following_users)

    # Récupérer les critiques associées à chaque demande de critique
    reviews = Review.objects.filter(ticket__in=tickets)

    context = {
        "tickets": tickets,
        "reviews": reviews,
    }
    return render(request, "pages/home.html", context)
