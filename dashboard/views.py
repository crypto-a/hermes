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
    if request.method == "POST":
        provider = request.POST["type"]          # "google", "microsoft", …
        # keep what the user typed; we’ll save it after the callback
        request.session["pending_email_ctx"] = {
            "display_name": request.POST["name"],
            "context":      request.POST.get("context", ""),
        }
        return redirect("mail:start_oauth", provider=provider)

    return render(request, "dashboard/add_account.html")