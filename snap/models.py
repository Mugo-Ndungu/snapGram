from django.db import models
from time import timezone
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
import PIL
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200,200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def delete_profile(self):
        self.delete()


class Post(models.Model):
    author = models.ForeignKey(User, related_name='post')
    photo = models.ImageField(upload_to='Posts_photos/')
    caption = models.CharField(max_length=60)

    def __str__(self):
        return self.author.username

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='liked_post')
    user = models.ForeignKey(User, related_name='liker')


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,self.user_to)

User.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))
