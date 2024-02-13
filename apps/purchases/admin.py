from django.contrib import admin

from apps.purchases.models import LinkPay, Purchase
from apps.purchases.service import generate_leadpay_payment_link


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["name_purcheses", "course", "status", "purchased_at", "price", "user", "id"]
    list_filter = ["status"]
    list_select_related = ["user", "course"]  # Оптимизация запроса
    search_fields = ["id", "course__name", "user__email", "user__first_name", "user__last_name"]

    @admin.display(description="покупки", ordering="id")
    def name_purcheses(self, obj):
        return f"Заказ №{obj.id}"


@admin.register(LinkPay)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["id", "link_pay"]

    @admin.display()
    def link_pay(self, obj):
        purch_obj = obj.purchase

        if obj.reference is None:
            link = generate_leadpay_payment_link(purch_obj)
            obj.reference = link
            obj.save(update_fields=["reference"])
            return link

        else:
            return obj.reference
