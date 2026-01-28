from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_message(*args, **kwargs):
    """Задача по отправле email"""

    send_mail(*args, **kwargs)
