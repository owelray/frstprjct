# Generated by Django 2.2.6 on 2019-12-16 15:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('second_project', '0005_auto_20191201_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]