from django.contrib import admin

from apps.purchases.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["name_purcheses", "course", "status", "purchased_at", "price", "user", "id"]
    list_filter = ["status"]
    list_select_related = ["user", "course"]  # Оптимизация запроса
    search_fields = ["id", "course__name", "user__email", "user__first_name", "user__last_name"]

    @admin.display(description="покупки", ordering="id")
    def name_purcheses(self, obj):
        return f"Заказ №{obj.id}"
