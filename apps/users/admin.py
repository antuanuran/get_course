from django.contrib import admin

from apps.purchases.models import Purchase
from apps.users.models import User


class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "favourites_courses", "purchases_courses", "id"]
    inlines = [PurchaseInline]
    filter_horizontal = ["groups", "user_permissions"]

    readonly_fields = ["favourites_courses", "available_courses"]

    # Запрещаем создавать Юзера через Админку
    def has_add_permission(self, request):
        return False
