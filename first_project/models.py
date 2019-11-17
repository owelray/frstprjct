from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=20, default="Unknown")
    age = models.IntegerField()

