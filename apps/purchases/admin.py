from django.contrib import admin

from apps.purchases.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["name_purcheses", "course", "purchased_at", "price", "user", "id"]
    list_select_related = ["user", "course"]  # Оптимизация запроса

    @admin.display(description="покупки", ordering="id")
    def name_purcheses(self, obj):
        return f"Заказ №{obj.id}"
