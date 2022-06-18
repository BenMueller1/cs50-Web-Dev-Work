from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/add", views.add_listing_to_watchlist, name="add_listing_to_watchlist"),
    path("listings/<int:listing_id>/remove", views.remove_listing_from_watchlist, name="remove_listing_from_watchlist"),
    path("listings/<int:listing_id>/bid", views.bid_on_listing, name="bid_on_listing"),
    path("listings/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("listings/<int:listing_id>/addComment", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.all_items_in_category, name="all_items_in_category"),
]
