from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=35)
    review = models.TextField(max_length=250)