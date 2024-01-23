from django.contrib import admin
from django.db.models import Count

from apps.courses.models import Course
from apps.purchases.models import Purchase
from apps.users.models import User


class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0
    autocomplete_fields = ["course"]


class FavouriteInline(admin.TabularInline):
    model = Course.favourites.through
    extra = 0
    autocomplete_fields = ["course"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "purchases_course_count", "favourites_course_count", "id"]
    inlines = [PurchaseInline, FavouriteInline]
    filter_horizontal = ["groups", "user_permissions"]
    readonly_fields = ["purchases_course_count", "favourites_course_count"]

    # Запрещаем создавать Юзера через Админку
    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(favourites_course_count=Count("favourites"), purchases_course_count=Count("purchases"))
        return qs

    @admin.display(description="favourite count", ordering="favourites_course_count")
    def favourites_course_count(self, obj: User) -> int:
        return obj.favourites_course_count

    @admin.display(description="purchase count", ordering="purchases_course_count")
    def purchases_course_count(self, obj: User) -> int:
        return obj.purchases_course_count
