from django.db import models
from datetime import datetime
# Create your models here.


class Comment(models.Model):
    teamID = models.CharField(max_length=100)
    guide = models.CharField(max_length=100)
    guide_email = models.CharField(max_length=100)
    body = models.TextField(null=True)
    published_date = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return self.teamID + 'Added Successfully'
