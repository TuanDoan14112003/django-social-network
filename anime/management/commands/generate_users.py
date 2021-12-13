from anime.models import Channel
from django.contrib.auth.models import User


from django.core.management.base import BaseCommand, CommandError
from anime.models import Post
class Command(BaseCommand):
    help = "Reset point_today field of model Post"
    def handle(self,*args,**kwargs):
        c1 = Channel.objects.get(slug='manga')
        c2 = Channel.objects.get(slug='anime')
        for i in range(51,100):
            print('creating user'+str(i))
            user = User.objects.create(username='user'+str(i),password='lol1411')
            c1.members.add(user)
            c2.members.add(user)
            print('add user to channels')
            user.save()
            c1.save()
            c2.save()
            user.save()