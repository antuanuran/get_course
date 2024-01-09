from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(_("email address"), unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),

        error_messages={
            "unique": _("A user with that username already exists."),
        },)
