# Generated by Django 3.2.7 on 2021-10-13 11:30

import anime.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0013_post_imagekit_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=anime.models.PathAndRename('testnewfolder')),
        ),
    ]
