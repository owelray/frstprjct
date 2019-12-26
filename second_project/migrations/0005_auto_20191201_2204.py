# Generated by Django 2.2.6 on 2019-12-01 20:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('second_project', '0004_auto_20191129_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='likedone',
            field=models.ManyToManyField(related_name='users_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='likenumber',
            field=models.IntegerField(default=0),
        ),
    ]