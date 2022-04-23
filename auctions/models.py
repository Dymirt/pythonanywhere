from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=20)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('auctions:category', args=[self.title])


class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(decimal_places=2, max_digits=10)

    objects = models.Manager()

    def __str__(self):
        return f'{self.user} bid {self.bid} on {self.listing}'


class Comment(models.Model):

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    objects = models.Manager()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f'Comment by {self.user} on {self.listing}'


def image_path(instance, filename):
    return 'listing_img/user_{0}//{1}'.format(instance.user.id, filename)


class ListingActiveManager(models.Manager):
    def get_queryset(self):
        return super(ListingActiveManager, self).get_queryset().filter(is_active=True)


class Listing(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ListingActiveManager()

    def __str__(self):
        return self.title

    def highest_bid(self):
        try:
            return max(self.bids.all(), key=lambda x: x.bid)
        except ValueError:
            return None

    # Use the get_absolute_url() method in templates to link to specific posts.
    def get_absolute_url(self):
        return reverse('auctions:listing', args=[self.pk])

    def close(self):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ['pk']


class User(AbstractUser):
    wishlist = models.ManyToManyField(Listing, blank=True, related_name="followers")

