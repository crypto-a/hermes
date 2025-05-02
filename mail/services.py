"""
High-level helpers consumed by views / Celery workers.
If you migrate to Celery or Dramatiq later, this stays the same.
"""

from __future__ import annotations
from .providers import get_provider
from .models import EmailAccount


def fetch_messages(account: EmailAccount, limit: int = 20):
    provider = get_provider(account.provider)
    return provider.list_messages(account, max_results=limit)


# Stub for your AI pipeline
def preprocess_email(message_meta):
    """
    Plug your LLM / classification / vector-store code here.
    Called **once** per message after fetch or webhook.
    """
    pass
