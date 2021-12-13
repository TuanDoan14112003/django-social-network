from django.core.management.base import BaseCommand, CommandError
from anime.models import Post
class Command(BaseCommand):
    help = "Reset point_today field of model Post"
    def handle(self,*args,**kwargs):
        print('Reseting all point_today for all posts')
        for post in Post.objects.all():
            print('Reseting point today for',post.id)
            post.point_today = 0;
            post.save()
        print("finish")
     