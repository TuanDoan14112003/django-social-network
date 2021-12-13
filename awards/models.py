from django.db import models
from pinax.badges.base import Badge, BadgeAwarded
from pinax.badges.registry import badges
from users.models import Profile,Point
from django.contrib.auth.models import Group

# Create your models here.

class PointsBadge(Badge):
    slug = "points"
    levels = [
        "Bronze",
        "Silver",
        "Gold",
    ]
    events = [
        "points_awarded",
    ]
    multiple = False

    def award(self, **state):

        user = state["user"]
        point = user.profile.total_point
        if point > 10000:
            return BadgeAwarded(level=3)
        elif point > 7500:
            return BadgeAwarded(level=2)
        elif point > 5000:
            return BadgeAwarded(level=1)
        
class ChannelAdminBadge(Badge):
    slug = "admin-privilege"
    levels = [
        "Admin Privilege"
    ]
    events = [
        "set_admin",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        point_instance = state["point_instance"]
        if point_instance.point > 200:
            #add admin privilege
            channel_staff_group = Group.objects.get(name="Staffs of "+point_instance.channel.name) # get staff group
            user.groups.add(channel_staff_group)
            return BadgeAwarded(level=1)

    


badges.register(PointsBadge)
badges.register(ChannelAdminBadge)