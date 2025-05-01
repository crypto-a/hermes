import hashlib
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard:index")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        _send_activation_email(request, user)
        return render(request, "accounts/email_confirmation_sent.html", {"user": user})

    return render(request, "accounts/register.html", {"form": form})


def _send_activation_email(request, user):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    url = request.build_absolute_uri(
        f"/accounts/activate/{uid}/{token}/"
    )
    context = {"activation_url": url, "user": user}
    body = render_to_string("accounts/email_activation.txt", context)
    print(user.email)
    send_mail(
        subject="Activate your Hermes account",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Your account is now active. Please log in.")
        return redirect("accounts:login")

    return render(request, "accounts/activate_failed.html")


@login_required
def profile_view(request):
    user_form_initial = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "username": request.user.username,
    }
    profile_form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile,
    )

    if request.method == "POST" and profile_form.is_valid():
        profile_form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "user_form": user_form_initial,  # read-only in the template
            "profile_form": profile_form,
            "gravatar": _gravatar_url(request.user.email),
        },
    )


def _gravatar_url(email, size=160):
    digest = hashlib.md5(email.lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?{urlencode({'s': str(size), 'd': 'identicon'})}"
