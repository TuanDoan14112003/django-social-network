from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib.auth.models import Group
from .models import Comment,Channel,Post, Vote, SubComment
import json
from .serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from guardian.shortcuts import assign_perm
import re
from django.contrib.auth.models import User
def send_notification(notification,recipient):
  channel_layer = get_channel_layer()
  channel = "comment_like_notifications_{}".format(recipient.username)
  async_to_sync(channel_layer.group_send)(
    channel, {
        "type": "notify",
        "command": "new_like_comment_notification",
        "notification": json.dumps(NotificationSerializer(notification).data)
      }
  )    
  
@receiver(post_save, sender=Comment)
def send_notification_comment(sender, instance, created, **kwargs):
    if created and instance.author != instance.original_post.author:
      author = instance.author
      recipient = instance.original_post.author
      notification = notify.send(action_object=instance,sender=author,recipient=recipient, actor=author, verb='commented on your post')[0][1][0]
      send_notification(notification = notification, recipient=recipient)

@receiver(post_save, sender=SubComment)
def send_notification_subcomment(sender, instance, created, **kwargs):
  if created:
    author = instance.author
    recipient = instance.parent_comment.author
    
    if instance.author != instance.parent_comment.author:
      notification = notify.send(action_object=instance,sender=author,recipient=recipient, actor=author, verb='replied your comment')[0][1][0]
      send_notification(notification = notification, recipient=recipient)


    regex_pattern = '(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)'
    tagged_usernames = re.findall(regex_pattern, instance.content)
    tagged_usernames = list(set(tagged_usernames))
    print(tagged_usernames)
    try:
      tagged_usernames.remove(recipient.username)
    except ValueError:
      pass
    for tagged_username in tagged_usernames:
      try:
        tagged_user = User.objects.get(username=tagged_username)
        tagged_notification = notify.send(action_object=instance,sender=author,recipient=tagged_user, actor=author, verb='mentioned you')[0][1][0]
        send_notification(notification = tagged_notification, recipient=tagged_user)
      except User.DoesNotExist:
        pass

  
    
    
    
@receiver(post_save,sender=Channel)
def create_admin_group(sender, instance, created, **kwargs):
  if created:
    new_admin_group = Group.objects.create(name="Staffs of " + instance.name)
    new_admin_group.save()
    instance.members.add(instance.creator)
    instance.moderators.add(instance.creator)
    instance.save()
    assign_perm('change_channel',new_admin_group,instance)
    
@receiver(post_save,sender=Post)
def set_vote(sender, instance, created, **kwargs):
  if created:
    vote = Vote.create(user=instance.author,
                    vote_object=instance,
                    vote_value=1)
    vote.save()


