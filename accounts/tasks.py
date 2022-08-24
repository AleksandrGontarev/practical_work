from time import sleep
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from celery import shared_task
from django.core.mail import send_mail as django_send_mail


@shared_task
def send_mail(subject, message, from_email):
    django_send_mail(subject, message, from_email, ['admin@example.com'])


@shared_task
def send_mail_to_admin():
    django_send_mail("subject", str(datetime.now()), "noreply@test.com", ['admin@example.com'])


