from django.contrib import admin
from django.db.models import Count

from .models import Category, Course, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    inlines = [ProductInline]


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ["name", "category", "id"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name_course", "tag_list", "poster", "price", "author", "is_sellable", "free"]
    list_filter = ["is_sellable"]
    filter_horizontal = ["favourites"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(tag_list=Count("tags"))
        return qs

    @admin.display(description="теги", ordering="tag_list")
    def tag_list(self, obj):
        return obj.tag_list

    @admin.display(boolean=True)
    def free(self, obj):
        return obj.free

    @admin.display(description="полное название курса")
    def name_course(self, obj):
        return obj.name
