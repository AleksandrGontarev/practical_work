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
def send_mail_to_user(subject, message):
    post = Post.objects.get(title=message)
    title = post.title
    pk = post.pk
    email = post.author.email
    link_post = "You have a new comment on the post: {title}\nLink post: http://127.0.0.1:8000/accounts/posts/{pk}".format(pk=pk, title=title)
    django_send_mail(subject, link_post, "blog_1@gmail.com", [email])

