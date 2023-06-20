from django.db import models


# Post model
class Post(models.Model):
    subreddit = models.CharField(max_length=255, null=False, name='subreddit')
    title = models.CharField(max_length=255, null=False, name='title')
    author = models.CharField(max_length=255, null=False, name='author')
    subtext = models.CharField(max_length=10000, null=False, name='subtext')
    permalink = models.CharField(max_length=255, null=False, name='permalink')
    url = models.URLField(null=False, name='URL')
    created = models.DateTimeField(null=False, name='created')
