import os

from celery.schedules import crontab

from django.urls import reverse_lazy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '7l%&6v6&rt(9hiy+=z$&f+ybm58o9_$pmmi=8+ljlk8ulfsij%'

DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_account@gmail.com'
EMAIL_HOST_PASSWORD = 'your account’s password'
DEFAULT_EMAIL_FROM = 'smtp.gmail.com'
