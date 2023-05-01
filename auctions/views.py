from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Bid, Listing, Comment

# Form for create listing page
class CreateListingForm(forms.ModelForm):
    """Creates form for Auction model."""
    title = forms.CharField(label="Title", max_length=20, required=True, widget=forms.TextInput(attrs={
                                                                            "autocomplete": "off",
                                                                            "placeholder": "Title",
                                                                            "aria-label": "title",
                                                                            "class": "form-control"
                                                                        }))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
                                    'placeholder': "Product Description",
                                    'aria-label': "description",
                                    'rows': 10,
                                    "class": "form-control"
                                    }))
    # photo = forms.ImageField(label="Photo", required=True, widget=forms.ClearableFileInput(attrs={
    #                                     "class": "form-control-file"
    #                                 }))
    photo = forms.URLField(label="Image URL", required=True, widget=forms.URLInput(attrs={
                                        "class": "form-control"
                                    }))
    category = forms.ChoiceField(required=True, choices=Listing.CATEGORIES, widget=forms.Select(attrs={
                                        "class": "form-control"
                                    }))
    price = forms.DecimalField(label="Price", required=True, widget=forms.NumberInput(attrs={
                                        "class": "form-control",
                                        "placeholder": "Starting Price"

                                    }))
    # date_created = forms.DateField(label="date_created", required=True, widget=forms.HiddenInput(attrs={
    #                                     "class": "form-control"
    # }))
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "photo", "price"]


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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
            # date_created = form.cleaned_data["date_created"]
            currentUser = request.user

            # Save a record
            listing = Listing(
                owner = currentUser,
                name = title,
                description = description,
                price = float(price),
                category = category,
                photo = photo,
                # date_created = date_created
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
