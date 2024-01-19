from django.contrib import admin

from apps.purchases.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["purchase", "course", "purchased_at", "price", "user", "id"]
    list_select_related = ["user", "course"]  # Оптимизация запроса
