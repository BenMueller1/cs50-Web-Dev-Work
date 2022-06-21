from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime

class Listing(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="listings", null=True)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    current_bid = models.OneToOneField('Bid', on_delete=models.CASCADE, related_name="listing", null=True)
    active = models.BooleanField(default=True)
    image_url = models.URLField(default=None)  # should this be a FilePathField ?
    category = models.CharField(max_length=30, default=None)


class User(AbstractUser):
    ''' since this inherits from AbstractUser, it already has field for username, email, password, etc.'''
    items_in_watchlist = models.ManyToManyField(Listing, blank=True)
    pass


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()
    related_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid", null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    posted_datetime = models.DateTimeField(default=datetime.now())