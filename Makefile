superuser:
	docker-compose down -v
	docker-compose up -d
	sleep 4
	python manage.py migrate
	python manage.py createsuperuser

run: superuser
	python manage.py runserver


min:
	python manage.py migrate
	python manage.py runserver
