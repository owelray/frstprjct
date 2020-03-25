from django.db import models


class Url(models.Model):
    long_url = models.URLField()
    short_url = models.URLField()
    use_bitly = models.BooleanField(default=False)
    url_hash = models.CharField(max_length=32, default=0)
    creator = models.CharField(max_length=32, default='Unknown')
    clicks_counter = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)

class Visitor(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=False, default='Unknown')
