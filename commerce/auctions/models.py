from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime

class User(AbstractUser):
    ''' since this inherits from AbstractUser, it already has field for username, email, password, etc.'''
    # TODO add a watchlist
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    current_price = models.FloatField()
    active = models.BooleanField(default=True)
    image_url = models.URLField(default=None)  # should this be a FilePathField ?
    category = models.CharField(max_length=30, default=None)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    posted_datetime = models.DateTimeField(default=datetime.now())