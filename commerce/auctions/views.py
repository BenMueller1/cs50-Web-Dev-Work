from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment


class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1000)
    starting_bid = forms.FloatField(min_value=0.01)
    image_url = forms.URLField(required=False)
    category = forms.CharField(required=False)


def index(request):
    return render(request, "auctions/index.html")


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
        print("got post request")
        # get data from form and add to listings
        #title, description, starting_bid, image_url, category
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        if "image_url" in request.POST.keys():
            image_url = request.POST['image_url']
        else:
            image_url = None
        if "category" in request.POST.keys():
            category = request.POST["category"]
        else:
            category = None

        new_listing = Listing(title=title, description=description, current_price=starting_bid, image_url=image_url, category=category, active=True)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {'form': form})