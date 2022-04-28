from django.contrib.auth.models import AbstractUser
from django.db import models
from requests import post

class User(AbstractUser):
    def amountOfFollowers(self):
        return Follow.objects.filter(followee = self).count()
    def amountOfFollowees(self):
        return Follow.objects.filter(follower = self).count()        

class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userPoster")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} posted {self.body} with title of {self.title}"

    def amountOfLikes(self):
        return Like.objects.filter(post = self).count()

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userFollower")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userFollowee")

    class Meta:
        unique_together = ["follower", "followee"]
    def __str__(self):
        return f"{self.follower} follows {self.followee}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likedPost")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLiker")
    class Meta:
        unique_together = ["post", "liker"]
    def __str__(self):
        return f"{self.liker} liked {self.post}"
