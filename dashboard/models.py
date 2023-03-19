from django.db import models

# Create your models here.


class Comment(models.Model):
    teamID = models.CharField(max_length=100)
    guide = models.CharField(max_length=100, null=True)
    guide_email = models.CharField(max_length=100, null=True)
    body = models.TextField(null=True)
    published_date = models.DateTimeField(auto_now_add=True, null=True)
