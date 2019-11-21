from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=35)
    review = models.TextField(max_length=250)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, default="1")