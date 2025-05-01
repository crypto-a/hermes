from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.


def profile_upload_to(instance, filename):
    return f"profiles/{instance.user.username}/{filename}"


class Profile(models.Model):
    """One-to-one extension of Django’s built-in User."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    picture = models.ImageField(
        upload_to=profile_upload_to,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
        help_text="JPEG / PNG • max 5 MB",
    )

    def __str__(self):
        return f"Profile<{self.user.username}>"
