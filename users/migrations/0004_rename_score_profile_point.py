# Generated by Django 3.2.7 on 2021-09-28 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='score',
            new_name='point',
        ),
    ]
