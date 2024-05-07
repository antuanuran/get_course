from django.contrib import admin

from .models import Report, VacancyData


@admin.register(VacancyData)
class VacancyDataAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "salary_min", "salary_max", "salary_avg", "link"]


@admin.register(Report)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["pdf", "created_at"]
