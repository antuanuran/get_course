# from time import sleep
from celery.app import shared_task
from django.core.files.base import File

from apps.vacancies import service
from apps.vacancies.models import Report, VacancyData
from salary_parser.salary_parser_beautifulsoup.scrapping_beautiful import main


@shared_task(autoretry_for=(Exception,), max_retries=1)
def vacancy_parser(course_name):
    data_all = main(course_name)
    for data_dict in data_all:
        vacancy, _ = VacancyData.objects.get_or_create(**data_dict)
        print(f" вакансия '{vacancy}' загружена в базу........ok")
    print("Загрузка в базу завершена, начинаем формировать ПДФ-Отчет...>")

    pdf_data = service.generate_report()
    Report.objects.create(pdf=File(pdf_data, name="report.pdf"))
    print("Отчет сформирован!")
