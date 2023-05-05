from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# model for bids
class Bid(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.user} just placed a bid for {self.price}"

# model for auction listings
class Listing(models.Model):
    CATEGORIES = (
    ('FA', 'Fashion'),
    ('FU', 'Furniture'),
    ('EL', 'Electronics'),
    ('MI', 'Miscellaneous'),
    ('KI', 'Kitchen'),
    ('DE', 'Decor'),
    ('SP', 'Sports'),
    ('TO', 'Toys'),
    ('HO', 'Home & Garden'),
    ('OT', 'Other')
    )

    photo = models.URLField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    category = models.CharField(max_length=2, choices=CATEGORIES, default=CATEGORIES[5][0])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")

    def __str__(self):
        return f"{self.name}: is {self.price} and is being sold by {self.owner}"

# model for comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")

    def __str__(self):
        return f"{self.user}: {self.comment}"

