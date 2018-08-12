release: python manage.py migrate
web: newrelic-admin run-program gunicorn newamericadotorg.wsgi --log-file -
worker: celery worker --app=newamericadotorg.celery.app
