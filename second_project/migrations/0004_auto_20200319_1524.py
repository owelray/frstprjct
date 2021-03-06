# Generated by Django 3.0.2 on 2020-03-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second_project', '0003_auto_20200318_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='creator',
            field=models.CharField(default='Unknown', max_length=32),
        ),
        migrations.AddField(
            model_name='url',
            name='unique_visitors',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='url',
            name='use_bitly',
            field=models.BooleanField(default=False),
        ),
    ]
