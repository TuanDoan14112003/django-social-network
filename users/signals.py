from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile,Point, Channel
from pinax.badges.registry import badges
from snsite import settings
from django.db.models.signals import m2m_changed

@receiver(post_save, sender=User)
def created_user(sender, instance, created, **kwargs):
  if created and instance.username != settings.ANONYMOUS_USER_NAME:
    new_profile = Profile(user=instance)
    new_profile.save()
    
@receiver(post_save, sender=Profile)
def change_profile(sender, instance, created, **kwargs):
  badges.possibly_award_badge("points_awarded", user=instance.user)
  
@receiver(post_save, sender=Point)
def set_admin_as_reward(sender, instance, created, **kwargs):
  if not instance.channel.created_by_user: #check if the channel is created by a user
    badges.possibly_award_badge("set_admin", user=instance.profile.user,point_instance=instance)
    
    
def add_member(sender,model,pk_set,instance,action, **kwargs):
    if action == 'post_add':
      print(kwargs)
      profile = User.objects.get(id=list(pk_set)[0]).profile
      try:
        point = Point.objects.get(channel=instance,profile=profile)
      except Point.DoesNotExist:
        point = Point.objects.create(channel=instance,profile=profile)
        point.save()

m2m_changed.connect(add_member, sender=Channel.members.through)
