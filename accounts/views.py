from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "accounts/login.html")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form,
            "username": request.user.username
            if request.user.is_authenticated
            else None,
        },
    )


@login_required
def subscription_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        if user_id:
            User = get_user_model()
            user_to_follow = User.objects.get(id=user_id)
            request.user.following.add(user_to_follow)
            return redirect(
                "home"
            )  # Rediriger vers la page souhaitée après l'abonnement

    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    context = {"users": users}
    return render(request, "accounts/subscriptions.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")
