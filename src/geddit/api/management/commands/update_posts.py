from django.core.management.base import BaseCommand, CommandError
from api.models import Post
import core.geddit as geddit


class Command(BaseCommand):

    # Update database for subreddit's listening
    def handle(self, *args, **options):
        try:
            headers = geddit.login()
            sub_list = geddit.get_subreddit_list()
            if not sub_list:
                return -1
            for sub in sub_list:
                posts = geddit.get(subreddit=sub, headers=headers)
                for post in posts:
                    Post.objects.get_or_create(**post)
        except ValueError:
            pass
