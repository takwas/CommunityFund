from django.db import models
from django.db.models import Max, Avg, Sum, Count
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, RegexValidator
from multiselectfield import MultiSelectField

# predefined interests
INTERESTS = ['Art', 'Comics', 'Crafts', 'Dance', 'Design', 'Fashion', 
        'Film', 'Food', 'Games', 'Journalism', 'Music', 'Photography', 
        'Publishing', 'Technology', 'Theater']

RATING = [1, 2, 3, 4, 5]

class UserProfile(models.Model):

    cc_regex = RegexValidator(r'^[0-9]*$', "Only numbers are allowed")

    user = models.OneToOneField(User)
    location = models.CharField("Location", max_length=100, blank=True)
    address = models.CharField("Address", max_length=50, blank=True, null=True)
    biography = models.TextField("Biography", max_length=140, blank=True, null=True)
    interests = MultiSelectField("Interests", max_choices=15, choices=[(x,x) for x in INTERESTS], blank=True)
    cc_number = models.CharField("CC Number", max_length=16, blank=True, validators=[cc_regex])
    
    def __repr__(self):
        return "{user: %s, location: %s, interests: %s}" % (self.user, self.location, self.interests)

    def __unicode__(self):
        return "user %s at %s is interested in %s" % (self.user, self.location, self.interests)

# auto create userprofile
def create_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)


class Community(models.Model):

    creator = models.ForeignKey(User)
    name = models.CharField("Name", max_length=100)
    location = models.CharField("Location", max_length=100)
    interests = MultiSelectField("Interests", max_choices=15, choices=[(x,x) for x in INTERESTS])

    def __repr__(self):
        return "{name: %s, location: %s, interests: %s}" % (self.name, self.location, self.interests)

    def __unicode__(self):
        return self.name


class Project(models.Model):
   
    # validators to ensure data is of appropriate length
    initiator = models.ForeignKey(User)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description", validators=[MaxLengthValidator(500)])
    community = models.ForeignKey(Community)
    funding_goal = models.DecimalField("Funding Goal", max_digits=19, decimal_places=2, 
        validators=[MinValueValidator(0)])
    current_funds = models.DecimalField("Current Funds", max_digits=19, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "{name: %s, initiator: %s, description: %s, community: %s}" \
                % (self.name, self.initiator, self.description, self.community)

    def __unicode__(self):
        return self.name

    def getCurrentFunds(self):
        # database sum query
        funds = Funded.objects.all().filter(project=self.id).aggregate(Sum('amount'))

        if not funds['amount__sum']:
            return 0
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
    rating = models.IntegerField(max_length=1, choices=[(x, str(x)) for x in RATING])
    
    def __repr__(self):
        return "{rated: %s, rater: %s, rating: %s}" % (self.rated, self.rater, self.rating)

    def __unicode__(self):
        return "%s rated %s as %s" % (self.rater, self.rated, self.rating)


class UserReputation(models.Model):
    
    rated = models.ForeignKey(User, related_name="user_rep")
    rater = models.ForeignKey(User)
    project = models.ForeignKey(Project) 
    rating = models.IntegerField(max_length=1, choices=[(x, str(x)) for x in RATING])

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


class Comment(models.Model):

    user = models.ForeignKey(User)
    community = models.ForeignKey(Community, related_name="comm_comments")
    text = models.CharField("Text", max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "{user: %s, community: %s, text: %s}" % (self.user, self.community, self.text)

    def __unicode__(self):
        return "%s member of %s commented %s" % (self.user, self.community, self.text)

