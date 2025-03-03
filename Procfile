release: python manage.py migrate
web: gunicorn newamericadotorg.wsgi --log-file -
worker: celery --app=newamericadotorg.celery.app worker --loglevel=INFO
