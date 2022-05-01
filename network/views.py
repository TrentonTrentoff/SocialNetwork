from sqlite3 import Timestamp
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    posts = paginator.page(page)
    return render(request, "network/index.html", {
        "posts": posts,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        body = request.POST["body"]
        newPost = Post(title=title, body=body, user=user)
        newPost.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, user):
    userProfile = User.objects.get(username=user)
    print(request.user)
    userIsFollower = False 
    if request.user.is_authenticated:
        currentUser = User.objects.get(username=request.user)
        # Checks if object has been created (i.e. if the current user follows the profiled user)
        if Follow.objects.filter(followee=userProfile, follower=currentUser.id).exists():
            userIsFollower = True
    else:
        currentUser = request.user
    posts = Post.objects.filter(user=userProfile).order_by('-timestamp')
    followers = Follow.objects.filter(followee=userProfile).values("follower_id")
    return render (request, "network/profile.html", {
        "userProfile": userProfile,
        "posts": posts,
        "followers": followers,
        "currentUser": currentUser,
        "userIsFollower": userIsFollower
    })

def following(request):
    currentUser = User.objects.get(username=request.user)
    followingUsers = Follow.objects.filter(followee = currentUser)
    followingUsersID = [follow.id for follow in followingUsers]
    posts = Post.objects.filter(user__in=followingUsersID)
    return render(request, "network/following.html", {
        "posts": posts
    })

def follow(request):
    if request.method == "POST":
        pass
        # Create follower, save as object, render profile page again, should say Unfollow instead of Follow