from django.core.management.base import BaseCommand
from accounts.models import User, Post, Comment
from faker import Faker


class Command(BaseCommand):
    help = 'This command is for inserting Author, Book, Publisher, Store into database.Insert 10, Authors, ' \
           '10 Publishers, 100 Books, 10 Stores. '

    def handle(self, *args, **options):

        fake = Faker()

        users = [User(username=fake.name(), password=fake.password(), email=fake.email(),
                      last_name=fake.last_name(), first_name=fake.first_name()) for _ in range(20)]
        User.objects.bulk_create(users)

        for user in User.objects.all():
            for i in range(10):
                posts = [Post(title=fake.sentence(), short_description=fake.sentence(50),
                              full_description=fake.text(300),
                              data_post=fake.date_between(start_date='-1y', end_date='today'), author=user)]

                Post.objects.bulk_create(posts)

        for post in Post.objects.all():
            for i in range(20):
                comments = [Comment(username=fake.name(), text_comment=fake.sentence(50),
                                    posts=post)]
                Comment.objects.bulk_create(comments)

