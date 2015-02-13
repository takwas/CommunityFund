from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):

    initiator = models.ForeignKey(User)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    funding_goal = models.DecimalField("Funding Goal", max_digits=19, decimal_places=2)
    current_funds = models.DecimalField("Current Funds", max_digits=19, decimal_places=2)
