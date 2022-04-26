from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userPoster")

    def __str__(self):
        return f"{self.user} posted {self.body} with title of {self.title}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userFollower")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userFollowee")

    def __str__(self):
        return f"{self.follower} follows {self.followee}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likedPost")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLiker")

    def __str__(self):
        return f"{self.liker} liked {self.post}"