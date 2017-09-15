.PHONY: run
run:
	@python manage.py runserver

.PHONY: run-prod
run-prod:
	@gunicorn jingpai.wsgi

.PHONY: migrate
migrate:
	@python manage.py migrate