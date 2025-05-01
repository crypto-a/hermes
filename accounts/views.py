from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        identifier = form.cleaned_data["identifier"]
        password = form.cleaned_data["password"]

        # username first
        user = authenticate(request, username=identifier, password=password)

        # then email
        if user is None:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(request,
                                    username=user_obj.username,
                                    password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            return redirect("dashboard:index")

        messages.error(request, "Invalid credentials – please try again.")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created! You can log in now.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})
