.PHONY: build
build:
	@python manage.py collectstatic --noinput&&python manage.py compiletemplates&&npm run build

.PHONY: build-prod
build-prod:
	@python manage.py collectstatic --noinput --settings=config.settings.production&&python manage.py compiletemplates --settings=config.settings.production&&npm run build-prod

.PHONY: run
run:
	@python manage.py runserver

.PHONY: run-prod
run-prod:
	@gunicorn config.wsgi

.PHONY: migrate
migrate:
	@python manage.py migrate

.PHONY: pylint
pylint:
	@pylint jingpai

.PHONY: report
report: pylint
	@flake8
