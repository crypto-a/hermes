"""
Abstract provider interface — each concrete adapter
(GmailProvider, OutlookProvider, …) must implement this.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from django.http import HttpRequest
from mail.models import EmailAccount
from mail.providers.types import MessageMeta


class BaseEmailProvider(ABC):
    slug: str                      # e.g. "google"
    friendly_name: str             # e.g. "Google Gmail"

    # ––––– OAuth ––––– #
    @classmethod
    @abstractmethod
    def get_authorize_url(cls, request: HttpRequest, state: str) -> str:
        """
        Returns the URL to redirect the user to for authorization.
        The state parameter is a random string that will be passed back
        to the callback URL.
        """
        ...

    @classmethod
    @abstractmethod
    def fetch_token(cls, request: HttpRequest, state: str) -> dict: ...
    # returns a dict with at least:
    #   { "access_token", "refresh_token", "expires_at", "email_address", "display_name" }

    # ––––– Data access ––––– #
    @classmethod
    @abstractmethod
    def list_messages(cls, account: EmailAccount, max_results: int = 20) -> list[MessageMeta]: ...
