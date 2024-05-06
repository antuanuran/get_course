# from time import sleep

from celery.app import shared_task

from apps.beautiful_soup.models import VacancyData

from .scrapping_beautiful import main


@shared_task(autoretry_for=(Exception,), max_retries=1)
def vacancy_parser():
    print("запускаем..")
    data_all = main()
    # print(data_all)
    for data_dict in data_all:
        vacancy, _ = VacancyData.objects.get_or_create(**data_dict)
        print(data_dict)
        print("************\n")
        # print(f" вакансия {vacancy} загружена в базу.")
