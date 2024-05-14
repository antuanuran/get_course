from urllib.parse import urljoin

from django.conf import settings
from django.db import models


class VacancyData(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    link = models.URLField(max_length=1500)
    salary_min = models.IntegerField(default=1, null=True, blank=True)
    salary_max = models.IntegerField(default=1, null=True, blank=True)
    salary_avg = models.IntegerField(default=1, null=True, blank=True)
    currency = models.CharField(max_length=10, default="руб.")

    class Meta:
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"

    def __str__(self) -> str:
        return self.name


class Report(models.Model):
    pdf = models.FileField(upload_to="files/report/", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_url(self) -> str:
        return urljoin(settings.BASE_PLATFORM_URL, self.pdf.url)


class CityStatus(models.Model):
    city = models.CharField(max_length=100)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
