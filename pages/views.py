from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from review.models import UserFollows, Ticket, Review


@login_required
def home_view(request):
    following_users = UserFollows.objects.filter(user=request.user).values(
        "followed_user"
    )
    tickets = Ticket.objects.filter(user__in=following_users).order_by("-time_created")
    reviews = Review.objects.filter(ticket__in=tickets).order_by("-time_created")
    context = {
        "tickets": tickets,
        "reviews": reviews,
    }
    print(context)
    return render(request, "pages/home.html", context)
