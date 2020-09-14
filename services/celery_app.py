from celery import Celery
from datetime import timedelta


celery_app = Celery('celery_app')

celery_app.conf.beat_schedule = {
    'backup': {
        'task': 'services.backup.database.backup_all',
        'schedule': timedelta(days=1),
        'args': None
    }
}

celery_app.autodiscover_tasks(['services.backup.database'])
