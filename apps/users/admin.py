from django.contrib import admin

from apps.purchases.models import Purchase
from apps.users.models import User


class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "id"]
    inlines = [PurchaseInline]
    filter_horizontal = ["groups", "user_permissions"]

    def has_add_permission(self, request):
        return False
