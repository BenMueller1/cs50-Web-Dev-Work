from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category


class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1000)
    starting_bid = forms.FloatField(min_value=0.01)
    image_url = forms.URLField(required=False)
    category = forms.CharField(required=False)


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {'listings': listings})


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


def create_listing_view(request):
    if request.method == "POST":
        user = request.user
        # get data from form and add to listings
        #title, description, starting_bid, image_url, category
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = Bid(amount=request.POST["starting_bid"], user=request.user)
        starting_bid.save()
        if "image_url" in request.POST.keys():
            image_url = request.POST['image_url']
        else:
            image_url = None
        if "category" in request.POST.keys():
            category = Category(name=request.POST["category"])
            category.save()
            # category = request.POST["category"]
        else:
            category = None

        new_listing = Listing(title=title, description=description, current_bid=starting_bid, image_url=image_url, category=category, active=True, creator=user)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {'form': form})

    
def listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    comments = reversed(listing.comments.all())  # reversed so that most recent comments are on top
    if listing in user.items_in_watchlist.all():
        in_watchlist = True
    else:
        in_watchlist = False
    return render(request, "auctions/listing.html", {"listing":listing, "in_watchlist":in_watchlist, "user":user, "comments":comments})


def add_listing_to_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    user.items_in_watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))


def remove_listing_from_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    user.items_in_watchlist.remove(listing)
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))


def bid_on_listing(request, listing_id):
    # should i add code to delete the old bid objects??
    user = request.user
    
    listing = Listing.objects.get(id=listing_id)
    bid_amount = request.POST["bid_amount"]
    if float(bid_amount) > listing.current_bid.amount:
        bid = Bid(user=user, amount=bid_amount, related_listing=listing)
        listing.current_bid = bid
        bid.save()
        listing.save()
    else: # bid is too small
        return HttpResponse("Bid must be greater than the current price.")
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))


def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.active = False
    listing.winner = listing.current_bid.user
    listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))


def add_comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    text = request.POST["comment_text"]
    comment = Comment(user=user, text=text, listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))


def watchlist(request):
    user = request.user
    watchlist_items = user.items_in_watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})