
from celery import Celery

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShopThing.settings')
app = Celery('ShopThing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()