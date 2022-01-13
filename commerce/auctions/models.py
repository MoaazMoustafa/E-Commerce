from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL
from django.db.models.fields import DateTimeField


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="pins/%y/%m/%d", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    starting_bid = models.FloatField()
    last_bid = models.FloatField(default=0)
    category = models.ForeignKey(
        'Category', on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=DO_NOTHING)
    listing = models.ForeignKey('Listing', on_delete=DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    class Meta:
        unique_together = ('user', 'listing', 'price')

    def __str__(self):
        return f"{self.user.username} ===> {self.listing.title}"


class Comment(models.Model):
    listing = models.ForeignKey('Listing', on_delete=DO_NOTHING)
    user = models.ForeignKey('User', on_delete=DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.user.username} commented on {self.listing} at {self.time}'


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} added {self.listing.title} to his watchlist '

    class Meta:
        unique_together = ('user', 'listing')
