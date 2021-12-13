from django.db import models
from django.contrib.auth.models import User
from anime.models import Channel
from django.urls import reverse
from anime.rename import PathAndRename
# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
  avatar = models.ImageField(upload_to=PathAndRename('user_pics'),default='default_user_avatar.jpg')
  cover = models.ImageField(upload_to=PathAndRename('user_pics'),default='default_channel_cover.jpg')
  total_point = models.IntegerField(default = 0)
  user_level = models.PositiveSmallIntegerField(default=0)
  description = models.TextField(max_length=500,blank=True, null=True)
  
  def award_points(self,points,channel):
    point_instance,created = Point.objects.get_or_create(channel=channel,profile=self)
    point_instance.point += points
    point_instance.save()
    self.total_point += points
    self.save()
  def get_absolute_url(self):
    return reverse('profile', kwargs={'pk': self.user.pk})
  def __str__(self):
    return "Profile cua " + self.user.username
  
class Point(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
  point = models.IntegerField(default = 0)
  
  
