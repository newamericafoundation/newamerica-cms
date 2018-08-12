release: python manage.py migrate
web: gunicorn newamericadotorg.wsgi --log-file -
worker: celery worker --app=newamericadotorg.celery.app
