# Generated by Django 3.2.7 on 2021-10-13 13:10

import anime.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0014_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=anime.models.PathAndRename('post_pics')),
        ),
    ]
