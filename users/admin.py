from django.contrib import admin
from .models import Profile,Point
# Register your models here.
myModels = [Profile,Point]  # iterable list
admin.site.register(myModels)


