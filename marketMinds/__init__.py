# this will make sure the app is always imported when
# django starts so that shared_task will use this app
from .celery import app as celery_app

__all__ = ('celery_app',)