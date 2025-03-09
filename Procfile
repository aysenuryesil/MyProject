web: gunicorn MyProject.wsgi --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
web: gunicorn MyProject.asgi:application -k uvicorn.workers.UvicornWorker
