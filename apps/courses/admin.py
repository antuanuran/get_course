from django.contrib import admin

from .models import Category, Course, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "id"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "tag_list", "poster", "price", "author", "is_sellable", "free"]
    list_filter = ["is_sellable"]
    filter_horizontal = ["favourites"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    @admin.display()
    def tag_list(self, obj: Course) -> list:
        return list(obj.tags.all())
