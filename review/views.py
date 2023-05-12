from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, UserFollows
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib import messages


@login_required
def create_ticket(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        ticket = Ticket.objects.create(
            title=title, description=description, user=request.user
        )
        ticket.save()
        # return redirect("ticket_detail", ticket.id)
    return render(request, "review/create_ticket.html")


@login_required
def tickets(request):
    all_tickets = Ticket.objects.all()
    context = {"tickets": all_tickets}
    return render(request, "review/tickets.html", context)


@login_required
def subscription_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        if user_id:
            User = get_user_model()
            user_to_follow = User.objects.get(id=user_id)

            # Vérifier si la relation existe déjà
            if UserFollows.objects.filter(
                user=request.user, followed_user=user_to_follow
            ).exists():
                messages.error(request, "Vous suivez déjà cet utilisateur.")
            else:
                userfollow = UserFollows(
                    user=request.user, followed_user=user_to_follow
                )
                userfollow.save()
                messages.success(
                    request, "Vous vous êtes abonné à cet utilisateur avec succès."
                )
                return redirect("subscription")

    User = get_user_model()
    users = User.objects.exclude(id=request.user.id).exclude(
        id__in=UserFollows.objects.filter(user=request.user).values("followed_user_id")
    )
    context = {"users": users}
    return render(request, "accounts/subscriptions.html", context)


from django.contrib import messages


@login_required
def unsubscribe(request, user_id):
    User = get_user_model()
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # Vérifier si la relation existe
    if UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow
    ).exists():
        UserFollows.objects.filter(
            user=request.user, followed_user=user_to_unfollow
        ).delete()
        messages.success(
            request, "Vous vous êtes désabonné de cet utilisateur avec succès."
        )
    else:
        messages.error(request, "Vous ne suivez pas cet utilisateur.")

    return redirect("subscription")
