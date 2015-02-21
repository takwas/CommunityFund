from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Community(models.Model):

    name = models.CharField("Name", max_length=100)
    location = models.CharField("Location", max_length=100)

    def __repr__(self):
        return (self.name, self.location)

    def __unicode__(self):
        return self.name


class Project(models.Model):
   
    initiator = models.ForeignKey(User)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    communty = models.ForeignKey(Community)
    funding_goal = models.DecimalField("Funding Goal", max_digits=19, decimal_places=2)
    current_funds = models.DecimalField("Current Funds", max_digits=19, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Funded(models.Model):

    project = models.ForeignKey(Project, null=True)
    user = models.ForeignKey(User, null=True)
    amount = models.DecimalField("Amount", max_digits=19, decimal_places=2)

    def __repr__(self):
        return (self.user, self.project, self.amount)

    def __unicode__(self):
        return "%s funded %s in amount %s" % (self.project, self.user, self.amount)


class UserInterests(models.Model):

    user = models.ForeignKey(User, name="user_interests")
    interest = models.CharField("Interest", max_length=100)

    def __repr__(self):
        return (self.user, self.interest)

    def __unicode__(self):
        return "user %s is interested in %s" % (self.user, self.interest)


class CommunityInterests(models.Model):
    
    community = models.ForeignKey(Community, related_name="comm_interests")
    interest = models.CharField("Interest", max_length=100)

    def __repr__(self):
        return (self.community, self.interest)

    def __unicode(self):
        return "%s community interested in %s" % (self.community, self.interest)


class ProjectReputation(models.Model):

    rated = models.ForeignKey(Project, related_name="project_rep")
    rater = models.ForeignKey(User) 
    rating = models.IntegerField("Rating", 
        validators=[MaxValueValidator(5),MinValueValidator(0)])

    def __repr__(self):
        return (self.rated, self.rater, self.rating)

    def __unicode__(self):
        return "%s rated %s as %s" % (self.rater, self.rated, self.rating)


class UserReputation(models.Model):
    
    rated = models.ForeignKey(User, related_name="user_rep")
    rater = models.ForeignKey(User) 
    rating = models.IntegerField("Rating", 
        validators=[MaxValueValidator(5),MinValueValidator(0)])

    def __repr__(self):
        return (self.rated, self.rater, self.rating)

    def __unicode__(self):
        return "%s rated %s as %s" % (self.rater, self.rated, self.rating)


class UserLocation(models.Model):

    user = models.ForeignKey(User)
    location = models.CharField("Name", max_length = 100)

    def __repr__(self):
        return (self.user, self.location)

    def __unicode__(self):
        return "user %s is located in %s" % (self.user, self.location)
    

class CommunityLocation(models.Model):
    
    community = models.ForeignKey(Community)
    location = models.CharField("Name", max_length = 100)

    def __repr__(self):
        return (self.user, self.location)

    def __unicode__(self):
        return "community %s is located in %s" % (self.community, self.location)
