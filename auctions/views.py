from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Bid, Listing, Comment
from .forms import *


def index(request):
    # set all active listings to listings variable and render them on index page
    form = CreateListingForm(request.POST)
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "form": form
    })


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

# allow users to create a new listing if logged in
@login_required(login_url="auctions:login")
def create_listing(request):
    """Create Listing view: allows to add new listing through a form."""
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Get all data from the form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            photo = form.cleaned_data["photo"]
            currentUser = request.user

            # Save a record
            listing = Listing(
                owner = currentUser,
                name = title,
                description = description,
                price = float(price),
                category = category,
                photo = photo,
            )
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": CreateListingForm(),
    })

# display all active listings for selected category
def show_category(request):
    if request.method == "POST":
        form = FilterCategoryForm(request.POST)
        if form.is_valid():
            selected_category = form.cleaned_data["category"]
            listings = Listing.objects.filter(is_active=True, category=selected_category)
            return render(request, "auctions/category.html", {
                "listings": listings,
                "category": selected_category,
            })
    else:
        # if the request method is GET, just render the category.html template
        form = FilterCategoryForm()
        
    return render(request, "auctions/category.html", {
        "form": form,
    })

# displays listing details for selected listing
def show_listing(request, id):
    listing = Listing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })

def remove_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse('listing', args=[str(id)]))

def add_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse('listing', args=(id,)))

# displays page with only items on a user's watchlist
def show_watchlist(request):
    user = request.user
    listings = user.user_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

# allows users to add comments to listings
def add_comment(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    comment = request.POST['comment']
    new_comment = Comment(
        user = user,
        listing = listing,
        comment = comment,
        )
    new_comment.save()
    return HttpResponseRedirect(reverse('listing', args=[str(id)]))
    