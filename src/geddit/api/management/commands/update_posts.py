from django.core.management.base import BaseCommand, CommandError
from api.models import Post
import core.geddit as geddit
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        headers = geddit.login()
        sub_list = geddit.get_subreddit_list()
        for sub in sub_list:
            posts = geddit.get(subreddit=sub, headers=headers)
            for post in posts:
                Post.objects.get_or_create(**post)