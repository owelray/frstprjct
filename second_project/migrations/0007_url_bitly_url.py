# Generated by Django 3.0.2 on 2020-03-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second_project', '0006_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='bitly_url',
            field=models.URLField(null=True),
        ),
    ]