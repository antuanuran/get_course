from django.contrib import admin, messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from ordered_model.admin import OrderedInlineModelAdminMixin, OrderedModelAdmin, OrderedTabularInline

from .models import (
    Category,
    Certificate,
    Comment,
    Course,
    Lesson,
    LessonTask,
    LessonTaskAnswer,
    Product,
    Review,
    UserAnswer,
)
from .tasks import send_certificate


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name_category", "count_products", "id"]
    inlines = [ProductInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(count_products=Count("products"))
        return qs

    @admin.display(description="кол-во линеек курсов", ordering="count_products")
    def count_products(self, obj):
        return obj.count_products

    @admin.display(description="направление", ordering="name_category")
    def name_category(self, obj):
        return obj.name


class LessonInline(OrderedTabularInline):
    model = Lesson
    extra = 0
    exclude = ["videos"]
    readonly_fields = ["move_up_down_links"]


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    autocomplete_fields = ["author"]


@admin.register(Course)
class CourseAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ["name_course", "sellable", "tag_list", "poster", "price", "author", "is_sellable", "free", "id"]
    list_filter = ["is_sellable"]
    list_editable = ["is_sellable"]
    filter_horizontal = ["favourites", "curators"]
    search_fields = ["name"]
    inlines = [LessonInline, ReviewInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(tag_list=Count("tags"))
        return qs

    @admin.display(description="теги", ordering="tag_list")
    def tag_list(self, obj):
        return obj.tag_list

    @admin.display(boolean=True, ordering="price")
    def free(self, obj):
        return obj.free

    @admin.display(description="название курса", ordering="name")
    def name_course(self, obj):
        return obj.name

    @admin.display(description="активировать / закрыть курс")
    def sellable(self, obj: Course):
        link = reverse("admin:sel", args=[obj.id])
        return mark_safe(f"<a href='{link}'>вкл/выкл</a>")

    def get_urls(self):
        urls = [
            path("<obj_id>/sellable/", self.sellable_viewset, name="sel"),
        ] + super().get_urls()
        return urls

    def sellable_viewset(self, request, obj_id, *args, **kwargs):
        obj = get_object_or_404(Course, id=obj_id)
        obj.is_sellable = not obj.is_sellable
        obj.save(update_fields=["is_sellable"])
        return redirect(reverse("admin:courses_course_changelist"))


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["created_at", "author", "course", "rating", "is_published", "id"]
    list_select_related = ["author", "course"]
    autocomplete_fields = ["author", "course"]
    list_filter = ["is_published", "created_at"]


class LessonTaskInline(admin.TabularInline):
    model = LessonTask
    extra = 0
    exclude = ["images", "videos", "links"]


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Lesson)
class LessonAdmin(OrderedModelAdmin):
    list_display = ["name_lesson", "course", "order", "move_up_down_links", "course_id", "task_list", "id"]
    readonly_fields = ["move_up_down_links"]
    inlines = [LessonTaskInline, CommentInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(task_list=Count("tasks"))
        return qs

    @admin.display(description="задания", ordering="task_list")
    def task_list(self, obj):
        return obj.task_list

    @admin.display(description="название урока", ordering="id")
    def name_lesson(self, obj):
        return obj.name


class LessonTaskAnswerInline(admin.TabularInline):
    model = LessonTaskAnswer
    extra = 0


@admin.register(LessonTask)
class LessonTaskAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "course", "auto_test", "id"]
    list_editable = ["auto_test"]
    inlines = [LessonTaskAnswerInline]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["task", "user", "success", "id"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["created_at", "lesson", "author", "text"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["course", "user", "pdf", "send_certificate", "created_at"]
    list_display_links = ["course", "user"]

    @admin.display(description="сертификат")
    def send_certificate(self, obj: Certificate):
        link = reverse("admin:send_certificate_email", args=[obj.id])
        return mark_safe(f"<a href='{link}'>Отправить на email</a>")

    def _send_certificate_email(self, request, object_id, *args, **kwargs):
        send_certificate(object_id)
        messages.info(request, "Отправлено")
        return redirect("admin:courses_certificate_changelist")

    def get_urls(self):
        urls = [
            path("<object_id>/send_email/", self._send_certificate_email, name="send_certificate_email"),
        ] + super().get_urls()
        return urls
