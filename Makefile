.PHONY: run
run:
	@python manage.py runserver

.PHONY: run-prod
run-prod:
	@gunicorn jingpai.wsgi

.PHONY: migrate
migrate:
	@python manage.py migrate

.PHONY: pylint
pylint:
	@pylint jingpai

.PHONY: report
report: pylint
	@flake8
