import os
from django.conf import settings
from celery import Celery

# set the default django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketMinds.settings')

app = Celery('marketMinds')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(f'django.conf:{settings.__name__}', namespace='CELERY')

# auto discover tasks for all registered django app configs.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


