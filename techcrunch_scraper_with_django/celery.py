import os

from celery import Celery


# Set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE',
                      value='techcrunch_scraper_with_django.settings')

app = Celery(main='techcrunch_scraper_with_django',
             broker=settings.CELERY_BROKER_URL)

app.config_from_object(obj='django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-60-seconds-scrape_remain_search_items': {
        'task': 'techcrunch.tasks.techcrunch_scrape_remain_search_item',
        'schedule': 60,  # In Second
    },
    'every-60-seconds-scrape_remain_auto_scrap_items': {
        'task': 'techcrunch.tasks.techcrunch_scrape_remain_auto_scrap_item',
        'schedule': 60,  # In Second
    },
    'every-86400-seconds-scrape_remain_auto_scrap_items': {
        'task': 'techcrunch.tasks.techcrunch_scrape_daily_item',
        'schedule': 60,  # In Second
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# celery -A techcrunch_scraper_with_django worker -l INFO -P eventlet
# celery -A techcrunch_scraper_with_django beat --loglevel=INFO
