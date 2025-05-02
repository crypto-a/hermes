from .gmail import GmailProvider

# Auto-discover & register
_ALL = [GmailProvider]
PROVIDERS = {p.slug: p for p in _ALL}

def get_provider(slug):
    return PROVIDERS[slug]
