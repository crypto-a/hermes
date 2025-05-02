from django.conf import settings
from django.db import models

# Create your models here.
class EmailAccount(models.Model):
    PROVIDER_CHOICES = [
        ("google", "Google Gmail"),
        ("microsoft", "Microsoft Outlook"),
        ("imap", "Generic IMAP"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="email_accounts")
    provider = models.CharField(max_length=32, choices=PROVIDER_CHOICES)
    email_address = models.EmailField()
    display_name = models.CharField(max_length=128, blank=True)
    # OAuth tokens (JSON blobs keep provider-specific extras)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    # free-form context the user typed in “Add account”
    context = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email_address} ({self.get_provider_display()})"