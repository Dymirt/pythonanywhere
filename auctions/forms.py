from django.forms import ModelForm, NumberInput, HiddenInput

from .models import Listing,  Bid, Comment


class ListingForm(ModelForm):

    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'starting_bid', 'image_url', 'user']
        widgets = {
            'starting_bid': NumberInput(attrs={'step': 0.01, 'min': 0}),
            'user': HiddenInput()
        }


class BidForm(ModelForm):

    class Meta:
        model = Bid
        fields = ['bid', 'user', 'listing']
        widgets = {
            'bid': NumberInput(attrs={'step': 0.01, 'min': 0}),
            'user': HiddenInput(),
            'listing': HiddenInput(),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'listing', 'text']
        widgets = {
            'user': HiddenInput(),
            'listing': HiddenInput()
        }
