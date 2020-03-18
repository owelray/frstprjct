from django.db import models

class Url(models.Model):
    long_url = models.URLField()
    use_bitly = models.BooleanField(default=False)
    short_url = models.CharField(max_length=32)
    clicks_counter = models.IntegerField(default=0)
