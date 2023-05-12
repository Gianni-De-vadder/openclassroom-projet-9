from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, UserFollows
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model


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
        print(user_id)
        if user_id:
            User = get_user_model()
            user_to_follow = User.objects.get(id=user_id)
            userfollow = UserFollows(user=request.user, followed_user=user_to_follow)
            userfollow.save()
            return redirect("subscription")

    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    context = {"users": users}
    return render(request, "accounts/subscriptions.html", context)
