from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    profile_image = models.ImageField(default='profile_images/default.jpg',upload_to="static/media/profile_images")
    bio = models.TextField(null=True ,blank=True ,max_length=500 ,default='')
    def get_num_posts(self):
        return Post.objects.filter(user=self).count()
    def is_following(self,followed):
        count = follow.objects.filter(follower=self,followed=followed).count()
        return count
    def get_num_followers(self):
        return follow.objects.filter(followed=self).count()
    def get_followings(self):
        following = follow.objects.filter(follower=self)
        temp = []
        for item in following:
          temp.append(item.followed.id)

        return temp

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=3000,null=False,blank=False)
    date_posted = models.DateTimeField(auto_now_add=True ,null=False)
    def __str__(self):
        return self.text

class follow(models.Model):
    followed = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return self.follower.username+"  ==>  "+ self.followed.username