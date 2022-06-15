from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ''' since this inherits from AbstractUser, it already has field for username, email, password, etc.'''
    # TODO add a watchlist
    pass

# TODO auction listing model

# TODO bid model

# TODO comment on auction listing model