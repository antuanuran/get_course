from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from apps.purchases.models import Purchase
from apps.purchases.service import generate_leadpay_payment_link


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["name_purcheses", "course", "status", "payment_link", "purchased_at", "price", "user", "id"]
    list_filter = ["status"]
    list_select_related = ["user", "course"]  # Оптимизация запроса
    search_fields = ["id", "course__name", "user__email", "user__first_name", "user__last_name"]

    @admin.display(description="покупки", ordering="id")
    def name_purcheses(self, obj: Purchase):
        return f"Заказ №{obj.id}"

    @admin.display(description="ссылка на оплату")
    def payment_link(self, obj: Purchase):
        if obj.status == obj.Status.COMPLETED:
            return "-"
        link = reverse("admin:my_link", args=[obj.id])
        return mark_safe(f"<a href='{link}' target='_blank'> Оплатить </a>")

    def get_urls(self):
        urls = [
            path("<object_id>/payment_link/", self._generate_leadpay_payment_link, name="my_link"),
        ] + super().get_urls()
        return urls

    def _generate_leadpay_payment_link(self, request, object_id, *args, **kwargs):
        obj = get_object_or_404(Purchase, id=object_id)
        link = generate_leadpay_payment_link(obj)
        return redirect(link)
