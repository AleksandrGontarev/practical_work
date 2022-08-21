from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Post(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE,)
    short_description = models.CharField(max_length=200)
    full_description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class Comment(models.Model):

    username = models.CharField(max_length=200)
    text_comment = models.TextField()
    posts = models.ForeignKey(Post, on_delete=models.CASCADE())

    def __str__(self):
        return self.text_comment
