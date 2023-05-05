from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("category", views.show_category, name="show_category"),
    path("listing/<int:id>", views.show_listing, name="listing"),
    path("removeWatchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("addWatchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.show_watchlist, name="show_watchlist"),
    path("addComment/<int:id>", views.add_comment, name="add_comment")
]
