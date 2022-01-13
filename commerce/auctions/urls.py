from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path('detail/<int:id>', views.detail_listing, name="detail"),
    path('place-bid/<int:id>', views.place_bid, name="place-bid"),
    path('comment/<int:id>', views.add_comment, name="add_comment"),
    path('watchlist/<int:id>', views.watchlist, name="watch-list"),
]
