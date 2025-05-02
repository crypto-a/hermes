from __future__ import annotations
import os, json, datetime as dt, uuid

from django.conf import settings
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


from .base import BaseEmailProvider
from mail.models import EmailAccount
from .types import MessageMeta

_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


class GmailProvider(BaseEmailProvider):
    slug           = "google"
    friendly_name  = "Google Gmail"

    # ––––– OAuth helpers ––––– #
    @classmethod
    def _flow(cls, request=None, redirect_uri=None) -> Flow:
        return Flow.from_client_config(
            {
                "web": {
                    "client_id":     settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                    "token_uri":     "https://oauth2.googleapis.com/token",
                }
            },
            scopes=_SCOPES,
            redirect_uri=redirect_uri,
        )

    @classmethod
    def get_authorize_url(cls, request, state):
        flow = cls._flow(
            redirect_uri=f"{settings.GOOGLE_REDIRECT_BASE}{reverse('mail:oauth_callback', args=[cls.slug])}"
        )
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            login_hint=request.GET.get("login_hint"),
            prompt="consent",
            state=state,
        )
        return auth_url

    @classmethod
    def fetch_token(cls, request, state):
        flow = cls._flow(
            redirect_uri=f"{settings.GOOGLE_REDIRECT_BASE}{reverse('mail:oauth_callback', args=[cls.slug])}"
        )
        flow.fetch_token(code=request.GET["code"])

        creds = flow.credentials  # google.oauth2.credentials.Credentials
        userinfo = build("oauth2", "v2", credentials=creds).userinfo().get().execute()

        return {
            "access_token":  creds.token,
            "refresh_token": creds.refresh_token,
            "expires_at":    dt.datetime.utcfromtimestamp(creds.expiry.timestamp()),
            "email_address": userinfo["email"],
            "display_name":  userinfo.get("name", ""),
        }

    # ––––– Gmail read helpers ––––– #
    @classmethod
    def _build_service(cls, account: EmailAccount):
        from google.oauth2.credentials import Credentials

        creds = Credentials(
            account.access_token,
            refresh_token=account.refresh_token,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )
        service = build("gmail", "v1", credentials=creds)
        return service

    @classmethod
    def list_messages(cls, account: EmailAccount, max_results=20):
        service = cls._build_service(account)
        resp = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max_results, q="")  # you can pass a query
            .execute()
        )
        out: list[MessageMeta] = []
        for msg in resp.get("messages", []):
            meta = service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
            headers = {h["name"]: h["value"] for h in meta["payload"]["headers"]}
            out.append(
                MessageMeta(
                    id=msg["id"],
                    subject=headers.get("Subject", "(no subject)"),
                    sender=headers.get("From", ""),
                    date=headers.get("Date", ""),
                    snippet=meta.get("snippet", ""),
                )
            )
        return out
