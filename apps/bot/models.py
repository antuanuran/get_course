from django.db import models

from apps.users.models import User


class TgUser(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tg_user")
    username = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    extra_data = models.JSONField(default=dict)
