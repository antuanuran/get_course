# from time import sleep

from celery.app import shared_task

from apps.beautiful_soup.models import VacancyData

from .scrapping_beautiful import main


@shared_task(autoretry_for=(Exception,), max_retries=1)
def vacancy_parser():
    data_all = main()
    for data_dict in data_all:
        vacancy, _ = VacancyData.objects.get_or_create(**data_dict)
        print(f" вакансия '{vacancy}' загружена в базу........ok")
    print("Загрузка завершена!")
