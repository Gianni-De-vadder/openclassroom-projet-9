from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, UserFollows, Review
from django.contrib.auth import get_user_model
from django.contrib import messages
from review.forms import ReviewForm, TicketReviewForm
from django.http import JsonResponse


@login_required
def create_ticket(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        ticket = Ticket.objects.create(
            title=title, description=description, user=request.user
        )
        ticket.save()
    return render(request, "review/create_ticket.html")


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user == request.user:
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            ticket = Ticket.objects.update(
                title=title, description=description, user=request.user
            )
            return redirect("tickets")
        else:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            context = {"ticket": ticket}
            return render(request, "review/update_ticket.html", context)
    else:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce ticket.")
        return redirect("home")


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    context = {"ticket": ticket}
    return render(request, "review/ticket_detail.html", context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user == request.user:
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce ticket.")

    return redirect("tickets")


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        review.delete()
        messages.success(request, "La review a été supprimé avec succès.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette review.")

    return redirect("home")


@login_required
def tickets(request):
    user = request.user
    user_tickets = Ticket.objects.filter(user=user).order_by("-time_created")
    user_reviews = Review.objects.filter(user=user).order_by("-time_created")
    context = {
        "tickets": user_tickets,
        "reviews": user_reviews,
    }
    return render(request, "review/tickets.html", context)


@login_required
def subscription_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        if user_id:
            User = get_user_model()
            user_to_follow = User.objects.get(id=user_id)

            # Vérifier si l'utilisateur essaie de s'abonner à lui-même
            if request.user == user_to_follow:
                messages.error(request, "Vous ne pouvez pas vous abonner à vous-même.")
            else:
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

    return render(request, "review/subscriptions.html")


def search_users(request):
    query = request.GET.get("query")
    users = []
    if query:
        User = get_user_model()
        users = User.objects.filter(username__icontains=query).values("id", "username")
    return JsonResponse(list(users), safe=False)


from django.contrib import messages


@login_required
def unsubscribe(request, user_id):
    User = get_user_model()
    user_to_unfollow = get_object_or_404(User, id=user_id)
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


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReviewForm(request.POST or None, ticket_title=ticket.title)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            print(review)  # Vérification dans la console
            return redirect("tickets")

    context = {
        "form": form,
        "ticket": ticket,
    }
    return render(request, "review/create_review.html", context)


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        if request.method == "POST":
            rating = request.POST["rating"]
            headline = request.POST["headline"]
            body = request.POST["body"]
            review = Review.objects.update(rating=rating, headline=headline, body=body)
            messages.success(request, "Le ticket a été supprimé avec succès.")
            return redirect("tickets")
        else:
            review = get_object_or_404(Review, id=review_id)
            context = {"review": review}
            return render(request, "review/update_review.html", context)
    else:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette critique.")
        return redirect("home")


@login_required
def update_ticket_review(request, review_id):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        rating = request.POST["rating"]
        headline = request.POST["headline"]
        body = request.POST["body"]
        review = Review.objects.update(rating=rating, headline=headline, body=body)
        ticket = Ticket.objects.update(
            title=title, description=description, user=request.user
        )
        return redirect("tickets")

    review = get_object_or_404(Review, id=review_id)
    context = {"review": review}
    return render(request, "review/update_ticket_review.html", context)


@login_required
def create_ticket_review(request):
    if request.method == "POST":
        form = TicketReviewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            body = form.cleaned_data["body"]
            rating = form.cleaned_data["rating"]
            ticket = Ticket.objects.create(
                title=title, description=description, user=request.user
            )
            review = Review.objects.create(
                ticket=ticket,
                rating=rating,
                headline=title,
                body=body,
                user=request.user,
            )
            return redirect("tickets")
    else:
        form = TicketReviewForm()

    context = {
        "form": form,
    }
    return render(request, "review/create_ticket_review.html", context)


def review_detail_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    context = {"review": review}
    return render(request, "review/review_detail.html", context)
