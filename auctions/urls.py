from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.ListingListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_auction, name="add_listing"),
    path("<int:listing_id>", views.listing_detail, name="listing"),
    path("wishlist", login_required(views.WishlistListView.as_view()), name="wishlist"),
    path("comment", views.comment, name="comment"),
    path('categories', views.categories, name='categories'),
    path('<str:category>-category', views.CategoryListingListView.as_view(), name='category'),
    path('mylistings', login_required(views.UserListingListView.as_view()), name='mylistings'),
    path('closelisting-<int:listing_id>', views.close_listing, name='closelisting')
]
