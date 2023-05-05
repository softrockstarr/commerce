from django import forms
from .models import *

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
    photo = forms.URLField(label="Image URL", required=False, widget=forms.URLInput(attrs={
                                        "class": "form-control"
                                    }))
    category = forms.ChoiceField(required=True, choices=Listing.CATEGORIES, widget=forms.Select(attrs={
                                        "class": "form-control"
                                    }))
    price = forms.DecimalField(label="Price", required=True, widget=forms.NumberInput(attrs={
                                        "class": "form-control",
                                        "placeholder": "Starting Price"

                                    }))
    
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "photo", "price"]

# Drop-down to filter by category 
class FilterCategoryForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category']
        widgets = {
            'category': forms.Select(choices=Listing.CATEGORIES)
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        labels = {
            "price": ("")
        }
        widgets = {
            "price": forms.NumberInput(attrs={
                "placeholder": "Bid",
                "min": 0.01,
                "max": 100000000000,
                "class": "form-control"
            })
        }
