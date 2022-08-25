# from time import sleep
from datetime import datetime
# import requests
# from bs4 import BeautifulSoup
from .models import User, Post
from celery import shared_task
from django.core.mail import send_mail as django_send_mail


@shared_task
def send_mail(subject, message, from_email):
    django_send_mail(subject, message, from_email, ['admin@example.com'])


@shared_task
def send_mail_to_user(subject, message, post_id):
    post = Post.objects.get(id=int(post_id))
    email = post.author.email
    django_send_mail(subject, message, "blog_1@gmail.com", [email])

