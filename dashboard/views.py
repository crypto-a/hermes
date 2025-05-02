from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from mail.models import EmailAccount
from mail.services import fetch_messages


@login_required
def index(request):
    return render(request, "dashboard/index.html")


@login_required
def inbox(request):
    accounts   = EmailAccount.objects.filter(user=request.user)
    categories = ["Primary", "Advertisements", "Notifications"]

    # naive: always show first account’s first 20 msgs
    first_msgs = fetch_messages(accounts.first()) if accounts else []

    return render(request, "dashboard/inbox.html",
                  {"categories": categories,
                   "accounts": accounts,
                   "emails": first_msgs})

@login_required
def add_account(request):
    """
    Displays the “Add account” form. When the user presses **Add & Connect**
    you will kick off your OAuth handshake in JS (or redirect-to-provider
    in Python).  Keep the view simple for now.
    """
    if request.method == "POST":
        # TODO: start OAuth here – you’ll redirect instead of re-rendering
        messages.success(request, "Redirecting you to consent…")
        return redirect("dashboard:index")

    return render(request, "dashboard/add_account.html")