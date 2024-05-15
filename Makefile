superuser:
	docker-compose down -v
	docker-compose up -d
	sleep 4
	python manage.py migrate
	python manage.py createsuperuser

run: superuser
	python manage.py import_data data_all/import.csv
	python manage.py runserver


bot:
	python manage.py start_bot

# celery:
#   celery -A skillsup worker

scrapy_all:
	scrapy runspider salary_parser/salary_parser_scrapy/spiders/headhunter.py

scrapy:
	scrapy runspider salary_parser_scrapy/spiders/headhunter.py
