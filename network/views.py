import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

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
    followingUsers = Follow.objects.filter(follower=currentUser).values('followee')
    print (followingUsers)
    followingUsersID = []
    for user in followingUsers:
        for key in user:
            followingUsersID.append(user[key])
    posts = Post.objects.filter(user__in=followingUsersID)
    return render(request, "network/following.html", {
        "posts": posts
    })

def follow(request, followee):
    follower = request.user
    followee = User.objects.get(username=followee)
    if Follow.objects.filter(followee=followee, follower=follower).exists():
        # Find follow object, delete, reload profile
        print("DELETING A FOLLOW")
        existingFollow = Follow.objects.get(followee=followee, follower=follower)
        existingFollow.delete()
        url = reverse("profile", kwargs={'user': followee})
        return HttpResponseRedirect(url)
    else:
        print("CREATING A NEW FOLLOW")
        newFollow = Follow(followee=followee, follower=follower)
        newFollow.save()
        url = reverse("profile", kwargs={'user': followee})
        return HttpResponseRedirect(url)
    # Create follower, save as object, render profile page again, should say Unfollow instead of Follow

@csrf_exempt
def edit(request):
    id = json.loads(request.id)
    print (id)
    newPost = json.loads(request.body)
    editedPost = Post.objects.get(id=id)
    editedPost.update(body=newPost)
    return JsonResponse({"message": "Email sent successfully."}, status=201)