# Generated by Django 3.2.7 on 2021-09-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover',
            field=models.ImageField(default='default_channel_cover.jpg', upload_to='user_pics'),
        ),
    ]