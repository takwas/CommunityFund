from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Project(models.Model):
    initiator = models.ForeignKey(User)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    funding_goal = models.DecimalField("Funding Goal", max_digits=19, decimal_places=2)
    current_funds = models.DecimalField("Current Funds", max_digits=19, decimal_places=2)

class Funded(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    amount = models.DecimalField("Amount", max_digits=19, decimal_places=2)

class UserInterests(models.Model):
    user = models.ForeignKey(User, name="user_interests")
    interest = models.CharField("Interest", max_length=100)

class CommunityInterests(models.Model):
    community = models.ForeignKey(Community, related_name="comm_interests")
    interest = models.CharField("Interest", max_length=100)

class Community(models.Model):
    name = models.CharField("Name", max_length=100)
    location = models.CharField("Location", max_length=100)

class ProjectReputation(models.Model):
    rated = models.ForeignKey(Project, related_name="project_rep")
    rater = models.ForeignKey(User) 
    rating = models.IntegerField("Rating", 
        validators=[MaxValueValidator(5),MinValueValidator(0)])

class UserReputation(models.Model):
    rated = models.ForeignKey(User, related_name="user_rep")
    rater = models.ForeignKey(User) 
    rating = models.IntegerField("Rating", 
        validators=[MaxValueValidator(5),MinValueValidator(0)])
       
class Like(models.Model):
    user = models.ForeignKey(User)
    interest = models.ForeignKey(Interests)

# TODO
#class Location(models.Model):
    

# TODO
#class CurrentlyAt(models.Model):
    

