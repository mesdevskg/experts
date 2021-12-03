import os
from smtplib import (
    SMTPServerDisconnected,
    SMTPConnectError,
)
from socket import gaierror

from celery import Celery
from django.core.mail import send_mail as django_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('experts')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return 0


@app.task(bind=True, max_retries=3)
def send_email(self, subject: str, message: str, recipient_list: list):
    try:
        res = django_mail(subject, message, None, recipient_list=recipient_list)
    except (SMTPConnectError, SMTPServerDisconnected) as exc:
        raise self.retry(exc=exc, countdown=3)
    except TimeoutError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
    except gaierror as exc:
        raise self.retry(exc=exc, countdown=3)
    return res
