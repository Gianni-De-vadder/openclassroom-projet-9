from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket


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
