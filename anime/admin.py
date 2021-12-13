from django.contrib import admin
from .models import *
# Register your models here.
myModels = [Post,Anime,Studio,Comment,Vote,Channel,SubComment]
admin.site.register(myModels)

