from celery import shared_task
from django.core.mail import send_mail


@shared_task(
    max_retries=3,
    default_retry_delay=60,
)
def send_message(*args, **kwargs):
    """Задача по отправле email"""

    send_mail(*args, **kwargs)
