from django.db import models
from time import timezone
from django.contrib.auth.models import User,AbstractBaseUser,BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}Profile'

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()


class Post(models.Model):
    author = models.ForeignKey(User,related_name='post')
    photo = models.ImageField(upload_to='Posts_photos/')
    caption = models.CharField(max_length=60)

    def __str__(self):
        return self.post

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

class Like(models.Model):
    post = models.ForeignKey(Post,related_name='liked_post')
    user = models.ForeignKey(User, related_name='liker')

