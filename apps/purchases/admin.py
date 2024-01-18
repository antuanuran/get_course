from django.contrib import admin

from apps.purchases.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "course", "purchased_at", "price"]
    list_select_related = ["user", "course"]
