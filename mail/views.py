from django.shortcuts import render

# Create your views here.
import uuid, json
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest
from django.utils import timezone

from .providers import get_provider
from .models import EmailAccount
from .services import fetch_messages


@login_required
def start_oauth(request: HttpRequest, provider: str):
    """
    Entry-point:  /mail/connect/google/?login_hint=foo@bar.com
    """
    prov_cls = get_provider(provider)
    state = uuid.uuid4().hex
    request.session["oauth_state"] = state
    url = prov_cls.get_authorize_url(request, state=state)
    return redirect(url)


@login_required
def oauth_callback(request: HttpRequest, provider: str):
    if request.GET.get("state") != request.session.get("oauth_state"):
        return HttpResponseBadRequest("State mismatch")

    prov_cls   = get_provider(provider)
    token_data = prov_cls.fetch_token(request, request.GET["state"])

    pending = request.session.pop("pending_email_ctx", {})  # ‹— grab what we stored

    EmailAccount.objects.update_or_create(
        user=request.user,
        email_address=token_data["email_address"],
        defaults={
            "provider":      provider,
            "display_name":  pending.get("display_name") or token_data["display_name"],
            "context":       pending.get("context", ""),
            "access_token":  token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_at":    token_data["expires_at"],
        },
    )
    return redirect("dashboard:inbox")


@login_required
def messages_api(request: HttpRequest, account_id: int):
    """
    AJAX endpoint → returns the last 20 messages for <account_id>.
    """
    account = get_object_or_404(EmailAccount, pk=account_id, user=request.user)
    messages = fetch_messages(account)
    payload = [m.__dict__ for m in messages]
    return JsonResponse(payload, safe=False)
