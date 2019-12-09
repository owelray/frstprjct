from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=35)
    review = models.TextField(max_length=250)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likenumber = models.IntegerField(default=0)
    likedone = models.ManyToManyField(User, related_name='users_likes')