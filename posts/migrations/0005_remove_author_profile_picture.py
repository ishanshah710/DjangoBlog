# Generated by Django 3.2.8 on 2021-10-21 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_author_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='profile_picture',
        ),
    ]
