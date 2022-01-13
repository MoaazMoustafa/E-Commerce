from django.contrib import admin

from auctions.models import Bid, Category, Comment, Listing, User, WatchList

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(WatchList)
