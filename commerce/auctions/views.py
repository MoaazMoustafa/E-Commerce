from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import ListingForm

from .models import Listing, User, Bid, Comment, WatchList


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# 3


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {'listings': listings})


def create_listing(request):
    form = ListingForm()
    if request.method == "GET":
        return render(request, 'auctions/create-listing.html', {'form': form})
    elif request.method == "POST":
        form = ListingForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')


def detail_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    count_bid = Bid.objects.filter(listing=listing).count()
    comments = Comment.objects.filter(listing=listing).order_by("-time")
    return render(request, 'auctions/detail-listing.html', {'listing': listing, 'count_bid': count_bid, 'comments': comments})


def place_bid(request, id):
    listing = get_object_or_404(Listing, id=id)
    count_bid = Bid.objects.filter(listing=listing).count()
    comments = Comment.objects.filter(listing=listing).order_by("-time")
    print(request.POST.get('bid'))
    if request.method == "POST":
        if request.POST.get('bid') == '':
            return render(request, 'auctions/detail-listing.html', {'listing': listing, 'count_bid': count_bid, 'comments': comments,
                                                                    'message': 'You did not place any bids', 'color': 'red'})

        if float(request.POST.get('bid')) <= listing.last_bid or float(request.POST.get('bid')) <= listing.starting_bid:
            return render(request, 'auctions/detail-listing.html', {'listing': listing, 'count_bid': count_bid, 'comments': comments,
                                                                    'message': 'You have to enter a greater bid', 'color': 'red'})

        elif float(request.POST.get('bid')) > listing.last_bid and float(request.POST.get('bid')) > listing.starting_bid:

            try:
                new_bid = Bid.objects.create(
                    user=request.user, listing=listing, price=float(request.POST.get('bid')))
                listing.last_bid = float(request.POST.get('bid'))
                listing.save()
                return render(request, 'auctions/detail-listing.html', {'listing': listing, 'count_bid': count_bid, 'comments': comments,
                                                                        'message': 'Your bid has been placed successfully', 'color': 'green'})

            except:
                return render(request, 'auctions/detail-listing.html', {'listing': listing, 'count_bid': count_bid, 'comments': comments,
                                                                        'message': 'You placed a bid with the same price before', 'color': 'red'})


def add_comment(request, id):
    listing = get_object_or_404(Listing, id=id)
    user = request.user
    print(user, listing, request.POST.get('comment_content'), '🌹🌹🌹🌹🌹')
    comment = Comment.objects.create(user=user, listing=listing,
                                     content=request.POST.get('comment_content'))
    # comment.save()
    # return render(request, 'auctions/detail-listing.html', {'listing': listing})
    return redirect(f'/detail/{id}')


def watchlist(request, id):
    # print(kwargs)
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=id)
        try:
            new_watchlist = WatchList.objects.create(
                listing=listing, user=request.user)
            return redirect(f'/detail/{id}')
        except:
            return redirect(f'/detail/{id}')
    else:
        watchlist_items = WatchList.objects.filter(
            user=request.user).order_by('-time')
        print(watchlist_items)
        return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})
