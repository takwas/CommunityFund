from django.db import models
from django.db.models import Max, Avg, Sum, Count
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    location = models.CharField("Location", max_length=100)
    interests = models.CharField("Interests", max_length=256)

    def __repr__(self):
        return "{user: %s, location: %s, interests: %s}" % (self.user, self.location, self.interest)

    def __unicode__(self):
        return "user %s at %s is interested in %s" % (self.user, self.location, self.interest)

# create a User profile upon access
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Community(models.Model):

    name = models.CharField("Name", max_length=100)
    location = models.CharField("Location", max_length=100)
    interests = models.CharField("Interests", max_length=256)

    def __repr__(self):
        return "{name: %s, location: %s, interests: %s}" % (self.name, self.location, self.interests)

    def __unicode__(self):
        return self.name


class Project(models.Model):
   
    initiator = models.ForeignKey(User)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    community = models.ForeignKey(Community)
    funding_goal = models.DecimalField("Funding Goal", max_digits=19, decimal_places=2, 
        validators=[MinValueValidator(0)])
    current_funds = models.DecimalField("Current Funds", max_digits=19, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "{name: %s, initiator: %s, description: %s, community: %s}" % (self.name, self.initiator, self.description, self.community)

    def __unicode__(self):
        return self.name

    def getCurrentFunds(self):
        funds = Funded.objects.all().filter(project=self.id).aggregate(Sum('amount'))
        return funds['amount__sum']


class Funded(models.Model):

    project = models.ForeignKey(Project, null=True)
    user = models.ForeignKey(User, null=True)
    amount = models.DecimalField("Amount", max_digits=19, decimal_places=2, 
        validators=[MinValueValidator(0)])

    def __repr__(self):
        return "{user: %s, project: %s, amount: %s}" % (self.user, self.project, self.amount)

    def __unicode__(self):
        return "%s funded %s in amount %s" % (self.user, self.project, self.amount)


class ProjectReputation(models.Model):

    rated = models.ForeignKey(Project, related_name="project_rep")
    rater = models.ForeignKey(User) 
    rating = models.IntegerField("Rating", 
        validators=[MaxValueValidator(5),MinValueValidator(0)])

    def __repr__(self):
        return "{rated: %s, rater: %s, rating: %s}" % (self.rated, self.rater, self.rating)

    def __unicode__(self):
        return "%s rated %s as %s" % (self.rater, self.rated, self.rating)


class UserReputation(models.Model):
    
    rated = models.ForeignKey(User, related_name="user_rep")
    rater = models.ForeignKey(User) 
    rating = models.IntegerField("Rating", 
        validators=[MaxValueValidator(5),MinValueValidator(0)])

    def __repr__(self):
        return "{rated: %s, rater: %s, rating: %s}" % (self.rated, self.rater, self.rating)

    def __unicode__(self):
        return "%s rated %s as %s" % (self.rater, self.rated, self.rating)


class Member(models.Model):

    user = models.ForeignKey(User)
    community = models.ForeignKey(Community, related_name="comm_member")

    def __repr__(self):
        return "{user: %s, community: %s}" % (self.user, self.community)

    def __unicode__(self):
        return "%s member of %s" % (self.user, self.community)
