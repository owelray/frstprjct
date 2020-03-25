# Generated by Django 3.0.2 on 2020-03-23 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('second_project', '0005_auto_20200319_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(default='Unknown', max_length=32)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='second_project.Url')),
            ],
        ),
    ]
