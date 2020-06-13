from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_mail_async(data: dict):
    send_mail(
        data['title'],
        data['message'],
        data['email_from'],
        [settings.DEFAULT_EMAIL_FROM],
        fail_silently=False,
    )
