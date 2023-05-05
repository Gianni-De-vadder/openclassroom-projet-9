from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    username = request.user.username
    return render(request, "home.html", {"username": username})
