import os
from celery import Celery
from django.apps import apps
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object(settings)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

# lancer le scheduler de Celery Beat
# app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE
app.conf.timezone = 'UTC'