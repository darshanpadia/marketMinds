import os
from celery import Celery

# set the default django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketMinds.settings')

app = Celery('marketMinds')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto discover tasks for all registered django app configs.
app.autodiscover_tasks(['dashboard'])

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


