from django.contrib import admin

from apps.utilities.models import BlacklistedWord


@admin.register(BlacklistedWord)
class BlacklistedWordAdmin(admin.ModelAdmin):
    list_display = ["word"]
