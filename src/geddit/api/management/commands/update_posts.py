from django.core.management.base import BaseCommand, CommandError
from api.models import Post
import core.geddit as geddit
import os

# Update database for subreddit's listening
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            headers = geddit.login()
            sub_list = geddit.get_subreddit_list()
            for sub in sub_list:
                posts = geddit.get(subreddit=sub, headers=headers)
                for post in posts:
                    Post.objects.get_or_create(**post)
        except ValueError:
            pass