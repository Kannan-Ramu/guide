from django.db import models

# Create your models here.


class BestTeam(models.Model):
    teamID = models.CharField(max_length=10
                              )

    def __str__(self):
        return self.teamID + ' Added Successfully!'
