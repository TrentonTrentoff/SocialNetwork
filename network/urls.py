
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("follow/<str:followee>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("<str:user>", views.profile, name="profile"),

    # API Routes
    path("edit", views.edit, name="edit"),
]
