import os
from celery import Celery
from celery.schedules import crontab
from pendulum import Duration
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('apps')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "daily_free": {
        "task": "apps.tasks.daily_free",
        "schedule": crontab(hour=0, minute=0),
    },
    "billing_schedule": {
        "task": "apps.tasks.billing_schedule",
        "schedule": Duration(minutes=1),
    },
}
